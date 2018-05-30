from django.shortcuts import render, HttpResponseRedirect, redirect
#from django.http import HttpResponse
#from django.template import loader
#from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import *
from Assign_Management.models import Upload
from Assign_Management.storage import OverwriteStorage
from django.contrib.auth import get_user_model
import sys,os,datetime,importlib,unittest,ast,inspect,timeout_decorator,mosspy
from RestrictedPython import compile_restricted,utility_builtins,PrintCollector
from RestrictedPython.Guards import full_write_guard,safe_builtins
from RestrictedPython.custom_builtins import custom_safe_builtins
from unittest import TextTestRunner
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()
# Create your views here.

sys.path.append(os.getcwd()+"/media")

####################### Utility #######################
def str_to_class(str):
    return getattr(sys.modules[__name__], str)

####################### url #######################

def CreateAssignment(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'CreateAssignment.html')


def AssignmentDetail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    return render(request, 'Home.html')



def GenerateAssign(request,classroom):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST" and request.FILES['upload_testcase']:
        OSS = OverwriteStorage()
        var = request.user.username
        Assignment = request.POST.get('asname', '')
        Assignment_Detail = request.POST.get('asdetail', '')
        Deadline = request.POST.get('dateInput','')
        Hint = request.POST.get('hint','')
        Timer = request.POST.get('timer','')
        #dsa = 'upload_testcase' in request.POST and request.POST['upload_testcase']
        asd = request.FILES.get('upload_testcase',False)
        asdf = request.FILES.get('upload_template',False)
        mode = request.POST.get('mode','')
        in_sys_file = OSS.save(asd.name, asd)
        in_sys_file = OSS.save(asdf.name, asdf)
        f = open(os.getcwd()+'/media/'+asd.name, 'r')
        dab = f.read()
        f.close()
        f = open(os.getcwd()+'/media/'+asdf.name, 'r')
        dabb = f.read()
        f.close()
        os.remove(os.path.join(settings.MEDIA_ROOT, asd.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, asdf.name))
        GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=dabb ,text_testcase_content=dab  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
        GenerateAssign_instance_temp = Quiz.objects.get(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=dabb ,text_testcase_content=dab  ,hint=Hint, mode=mode, classroom=ClassRoom.objects.get(className=classroom))
        get_tracker = QuizTracker.objects.filter(classroom=GenerateAssign_instance_temp.classroom) #reference at QuizTracker
        for k in get_tracker:
            QuizStatus.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                                studentId=k.studentId,
                                                classroom=GenerateAssign_instance_temp.classroom,
                                                status=False,
                                                )
        if Timer != '':
            #print("timeryes")
            Timer_temp = ''
            for i in Timer:
                if i == ' ':
                    pass
                else:
                    Timer_temp += i
            Timer = Timer_temp
            o = Timer.split(':')
            x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
            for j in get_tracker:
                QuizTimer.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                         studentId=j.studentId,
                                         classroom=GenerateAssign_instance_temp.classroom,
                                         timer=x,
                                         )

        return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
    else:
        return render(request, 'CreateAssignment.html')


def DeleteAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    quiz = Quiz.objects.get(pk=quiz_id)
    quizStatus = QuizStatus.objects.filter(quizId=quiz, classroom=quiz.classroom, )
    for j in quizStatus:
        if j.status:
            quizDoneCount = QuizTracker.objects.get(
                            studentId=j.studentId,
                            classroom=quiz.classroom, )
            #print(quizDoneCount)
            if quizDoneCount.quizDoneCount != 0:
                try:
                    quizDoneCount.quizDoneCount -= 1
                    quizDoneCount.save(update_fields=["quizDoneCount"])
                except quizDoneCount.DoesNotExist:
                    pass
        elif j.status is not True:
            pass
    quiz.delete()
    return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

def regen(require_regen):
    test_temp = Quiz.objects.create(
        quizTitle=require_regen["quizTitle"],
        quizDetail=require_regen["quizDetail"],
        deadline=require_regen["deadline"],
        hint=require_regen["hint"],
        text_testcase_content=require_regen["text_testcase_content"],
        text_template_content=require_regen["text_template_content"],
        mode=require_regen["mode"],
        classroom=require_regen["classroom"]
    )
    GenerateAssign_instance_temp = test_temp
    get_tracker = QuizTracker.objects.filter(
        classroom=GenerateAssign_instance_temp.classroom)  # reference at QuizTracker
    for k in get_tracker:
        QuizStatus.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                            studentId=k.studentId,
                                            classroom=GenerateAssign_instance_temp.classroom,
                                            status=False,
                                            )
    print("k1 has passed")
    try:
        for k in get_tracker:
            tracker = QuizTracker.objects.get(studentId=k.studentId,
                                              classroom=GenerateAssign_instance_temp.classroom,
                                              )
            if tracker.quizDoneCount > 0:
                tracker.quizDoneCount -= 1
            tracker.save(update_fields=["quizDoneCount"])

        if require_regen["Timer"] != '':
            print("timeryes")
            Timer_temp = ''
            for i in require_regen["Timer"]:
                if i == ' ':
                    pass
                else:
                    Timer_temp += i
            require_regen["Timer"] = Timer_temp
            o = require_regen["Timer"].split(':')
            x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
            for j in get_tracker:
                QuizTimer.objects.update_or_create(quizId=GenerateAssign_instance_temp,
                                                   studentId=j.studentId,
                                                   classroom=GenerateAssign_instance_temp.classroom,
                                                   timer=x,
                                                   )
        print("k2 has passed")
    except Exception as e:
        print("k2 has failed")
        print(e)
        pass
    return test_temp

def EditAssign(request, classroom, quiz_id):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST":
        quiz = Quiz.objects.get(pk=quiz_id)
        OSS = OverwriteStorage()
        var = request.user.username
        Assignment = request.POST.get('asname', '')
        Assignment_Detail = request.POST.get('asdetail', '')
        Deadline = request.POST.get('dateInput', '')
        Hint = request.POST.get('hint', '')
        Timer = request.POST.get('timer', '')
        asd = request.FILES.get('upload_testcase', False)
        asdf = request.FILES.get('upload_template', False)
        mode = request.POST.get('mode', '')
        redo = request.POST.get('redo', '')
        in_sys_file = OSS.save(asd.name, asd)
        in_sys_file = OSS.save(asdf.name, asdf)
        f = open(os.getcwd()+"/media/" + asd.name, 'r')
        dab = f.read()
        f.close()
        f = open(os.getcwd()+"/media/" + asdf.name, 'r')
        dabb = f.read()
        f.close()
        os.remove(os.path.join(settings.MEDIA_ROOT, asd.name))
        os.remove(os.path.join(settings.MEDIA_ROOT, asdf.name))
        ### Define Section ###
        #if (Assignment != quiz.quizTitle or dab != quiz.text_testcase_content:
        quiz_old = {
        "title":quiz.quizTitle,
        "testcase":quiz.text_testcase_content,
        }
        if (redo == "Yes" or quiz_old["title"] != Assignment or quiz_old["testcase"] != dab):
            quiz.delete()
            require_regen = {"quizTitle":Assignment,
                             "quizDetail":Assignment_Detail,
                             "deadline":Deadline,
                             "hint":Hint,
                             "text_testcase_content":dab,
                             "text_template_content":dabb,
                             "mode":mode,
                             "classroom":quiz.classroom,
                             "Timer":Timer,
                             }
            regen(require_regen)
            print("ppl=sh!t")

        else:
            get_tracker = QuizTracker.objects.filter(
                classroom=quiz.classroom)  # reference at QuizTracker
            quiz.quizTitle = Assignment
            quiz.quizDetail = Assignment_Detail
            quiz.deadline = Deadline
            quiz.hint = Hint
            quiz.text_testcase_content = dab
            quiz.text_template_content = dabb
            quiz.mode = mode
            quiz.save()
            if Timer != '':
                # print("timeryes")
                Timer_temp = ''
                for i in Timer:
                    if i == ' ':
                        pass
                    else:
                        Timer_temp += i
                Timer = Timer_temp
                o = Timer.split(':')
                x = int(o[0]) * 3600 + int(o[1]) * 60 + int(o[2])
                for j in get_tracker:
                    timer = QuizTimer.objects.get(quizId=quiz_id,
                                                  studentId=j.studentId,
                                                  classroom=quiz.classroom,
                                                  )
                    if timer.start:
                        timer.timer = x
                        timer.timer_stop = timezone.now() + timezone.timedelta(seconds=timer.timer)
                    else:
                        timer.timer = x
                        timer.timer_stop = None
                    timer.save(update_fields=["timer", "timer_stop"])
        return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

    else:
        quiz = Quiz.objects.get(pk=quiz_id)
        try:
            quizTimer = QuizTimer.objects.get(quizId=quiz)
        except:
            quizTimer = ''
        context = {'quizedit': quiz,
                   'quiztedit': quizTimer,
                   'quizdedit': quiz.deadline,
                  }
        return render(request, 'EditAssignment.html', context)

#@timeout_decorator.timeout(5, use_signals=False)
def uploadgrading(request, classroom, quiz_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')

    elif ClassRoom.objects.get(className=classroom).user.filter(username=request.user.username).exists() != True:
        return HttpResponseRedirect('/ClassRoom/' + request.session["classroom"])

    from autograder_sandbox import AutograderSandbox
    global deadline, timer_stop
    timezone.make_aware(datetime.datetime.now(), timezone.get_default_timezone())
    t = timezone.localtime(timezone.now())  # offset-awared datetime
    t.astimezone(timezone.utc).replace(tzinfo=None)
    quiz = Quiz.objects.get(pk=quiz_id)
    try:
        Timer = QuizTimer.objects.get(quizId=quiz,
                                        studentId=User.objects.get(studentId=request.user.studentId),
                                        classroom=quiz.classroom,
                                        ).timer_stop
    except ObjectDoesNotExist:
        Timer = None
    #set utc+7 check setting file 'Asia/Bangkok'
    if Timer is not None:
        #print("Timer is not None.")
        deadline, timer_stop = timezone.localtime(quiz.deadline),timezone.localtime(Timer)
        deadline.astimezone(timezone.utc).replace(tzinfo=None)
        timer_stop.astimezone(timezone.utc).replace(tzinfo=None)
        if t >= deadline or t >= timer_stop:
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])
    elif Timer is None:
        #print("Timer is None.")
        deadline =  timezone.localtime(quiz.deadline)
        deadline.astimezone(timezone.utc).replace(tzinfo=None)
        #print(t)
        #print(deadline)
        if t >= deadline:
            return HttpResponseRedirect('/ClassRoom/'+request.session["classroom"])

    try:
        code_temp = ""
        if request.method == "POST" and 'time_left' in request.POST:
            #print("this?")
            time_left = request.POST.get("time_left",'')
            #print(time_left)
            try:
                timer = QuizTimer.objects.get(
                    quizId=quiz,
                    studentId=User.objects.get(studentId=request.user.studentId),
                    classroom=quiz.classroom, )
                timer.timer = time_left
                timer.save(update_fields=["timer"])
            except ObjectDoesNotExist:
                pass
            return render(request, 'Home.html')

        elif request.method == 'POST' and 'upload_submit' in request.POST:
            if request.FILES['upload']:
                #print("in_upload_submit")
                uploaded_to_file = request.FILES['upload']
                fileName = str(request.user.studentId) + '_uploaded_' + str(quiz.quizTitle) + '_' + str(quiz.classroom.className)+ uploaded_to_file.name[-3:]
                #OSS = OverwriteStorage()
                #in_sys_file = OSS.save(fileName, uploaded_to_file)
                fuck_sake = Quiz.objects.get(id=quiz_id)
                in_sys_file_location = os.getcwd()+"/media/"#+fuck_sake.classroom.className+'/'+request.user.studentId+'/'+fuck_sake.quizTitle+'/'
                temp_test = fuck_sake.classroom.className+'/'+request.user.studentId+'/'+fuck_sake.quizTitle+'/'
                sys.path.append(in_sys_file_location)
                FSS = FileSystemStorage()#(location=in_sys_file_location,
                                        #base_url=os.path.join(temp_test))
                in_sys_file = FSS.save(fileName, uploaded_to_file)
                in_sys_file_url = FSS.url(in_sys_file)
                print(FSS.path(in_sys_file))
                Upload.objects.get_or_create(title=in_sys_file, Uploadfile=in_sys_file ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                write_mode = False
                test_case_count = 0
                Out_count = 0
                score_total = 0
                max_score = 0
                # open file .txt. Address  file ???????? Now! change follow your PC
                with open(in_sys_file_location + in_sys_file, 'r+') as f:
                    code_final = code = f.read()
                    f.seek(0, 0)
                    for line in quiz.text_testcase_content.splitlines():
                        if "# Lib" in line:
                            f.write("import ".rstrip('\r\n') + line[6:].rstrip('\r\n') + '\n' + code)
                            break
                try:
                    restricted_globals = dict(__builtins__=safe_builtins)
                    byte_code = compile_restricted(code, filename='./media/' + in_sys_file, mode='exec')
                    exec(byte_code,restricted_globals,{})
                except Exception as E:
                    pass
                if in_sys_file[:-3] in sys.modules:
                    del sys.modules[in_sys_file[:-3]]
                    #importlib.invalidate_caches()
                    prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                else:
                    prob = importlib.import_module(in_sys_file[:-3])
                    #importlib.reload(prob)
                #print(prob)
                f = open(in_sys_file_location + in_sys_file, 'a')
                case = quiz.text_testcase_content
                f.write("\n\n")
                for case_line in case.splitlines():
                    if (case_line[:11] == "# Test case"):
                        test_case_count += 1
                        globals()['case_%s_result' % str(test_case_count)] = ""
                        Out_count += 1
                    f.write(case_line + "\n")
                for i in range(test_case_count):
                    i += 1
                    globals()['test_case_out_%s' % i] = ""
                    globals()['out_%s' % i] = ""
                with open(in_sys_file_location + in_sys_file, 'r') as f:
                    code = f.read()

                for line in code.splitlines():
                    if "# Stop" in line:
                        #print("stop")
                        write_mode = False
                    elif write_mode:
                        if "# Out" in line:
                            globals()['out_%s' % test_case_num] = eval(line[6:])
                        elif "# Score" in line:
                            #print("SOCREEEE")
                            globals()['score_%s' % test_case_num] = float(eval(line[8:]))
                        elif "# Break" in line:
                            #print("Break!")
                            write_mode = False
                        elif "prob." in line:
                            command = line
                            #print("command this line")
                            #print(command)
                            '''try:
                                exec_command = inspect.getsource(eval(command[:-4]))
                                byte_code = compile_restricted(exec_command, '<inline>', 'exec')
                                print(byte_code)
                                exec(byte_code, {'__builtins__': utility_builtins}, {})
                            except Exception as E:
                                print(E)
                                continue'''
                        try:
                            globals()['test_case_out_%s' % test_case_num] = eval(command)

                        except Exception as E:
                            print(E)
                            continue

                    elif "# Test case" in line:
                        #print("in testcase  ")
                        test_case_num = str(line[11])
                        write_mode = True
                #define
                for i in range(test_case_count):
                    i += 1
                    max_score += + globals()['score_%s' % i]
                # unittest process.
                class MyTestCase(unittest.TestCase): pass
                case_result = {}
                for i in range(1, test_case_count + 1, 1):
                    string = "def test_text_{0}(self):\n" \
                                  "    self.text_{0} = test_case_out_{0}\n" \
                                  "    self.mt_{0} = out_{0}\n" \
                                  "    if self.text_{0} == self.mt_{0}:\n" \
                                  "        globals()['case_{0}_result'] = 'PASS'\n" \
                                  "    else:\n" \
                                  "        globals()['case_{0}_result'] = 'FAIL'\n" \
                                  "        globals()['score_{0}'] = 0\n" \
                                  "    self.assertEquals(self.text_{0}, self.mt_{0})\n".format(i)
                    eval(compile(string, '<string>', 'exec'), globals())
                    setattr(MyTestCase, "test_text_{0}".format(i), str_to_class('test_text_{0}'.format(i)))
                    #case_result["test_text_{0}".format(i)] = globals()['case_{0}_result'.format(i)]
                    #from types import MethodType
                    #MyTestCase.test_text_1 = MethodType(test_text_1,MyTestCase)
                    #print(eval("'test_text_{0}'.format(i)"))
                    #method_list = [func for func in dir(MyTestCase) if
                                   #callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    #print(method_list)
                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                x = len(test_result.failures)
                for i in range(1, test_case_count + 1, 1):
                    case_result["test_text_{0}".format(i)] = globals()['case_{0}_result'.format(i)]
                print(case_result)
                if quiz.mode == "Pass or Fail" and x == 0:
                    result = "PASS"
                    result_model = 10
                    max_score = 10
                elif quiz.mode == "Pass or Fail" and x != 0:
                    result = "FAIL"
                    result_model = 0
                    max_score = 10
                elif quiz.mode == "Scoring":
                    for i in range(test_case_count):
                        i += 1
                        score_total = score_total + globals()['score_%s' % i]
                    result = "PASS"
                    result_model = 0
                else:
                    result = "FAIL"
                    result_model = 0
                case_result["result"] = result
                result_set = {'result':case_result,
                              'scoring':{'total_score':score_total,'max_score':max_score}
                              }
                if QuizStatus.objects.get(quizId=quiz, studentId=User.objects.get(studentId=request.user.studentId), classroom=quiz.classroom).status == False:
                    QuizTracker.objects.update_or_create(
                        studentId=User.objects.get(studentId=request.user.studentId),
                        classroom=quiz.classroom,
                    )
                    quizDoneCount = QuizTracker.objects.get(studentId=User.objects.get(studentId=request.user.studentId),
                                            classroom=quiz.classroom, )
                    quizDoneCount.quizDoneCount += 1
                    quizDoneCount.save()
                    quizStatus = QuizStatus.objects.get(quizId=quiz,
                                                       studentId=User.objects.get(studentId=request.user.studentId),
                                                       classroom=quiz.classroom,
                                                       )
                    quizStatus.status = True
                    quizStatus.save()
                #print(str(test_case_count) + ' ' + str(Out_count))
                for i in range(test_case_count):
                    i += 1
                    globals()['test_case_out_%s' % i] = ""
                    globals()['out_%s' % i] = ""
                    globals()['score_%s' % i] = 0
                test_case_count = 0
                Out_count = 0
                with open(in_sys_file_location + in_sys_file, 'w') as f:
                    f.write(code_final)
                f = open(in_sys_file_location + in_sys_file, 'r')
                try:
                    quiz_score = QuizScore.objects.get(quizId=quiz,
                                                       studentId=User.objects.get(studentId=request.user.studentId),
                                                       classroom=quiz.classroom)
                    if quiz.mode == "Scoring":
                        if score_total >= quiz_score.total_score:
                            print(str(quiz_score.total_score) + ":" + str(quiz_score.passOrFail))
                            print(str(score_total)+":"+str(result_model))
                            #return None
                            quiz_score.total_score = score_total
                            quiz_score.passOrFail = result_model
                            quiz_score.max_score = max_score
                            quiz_score.code =  Upload.objects.get(title=in_sys_file) #f.read()
                            quiz_score.save()
                    else:
                        if result_model >= quiz_score.passOrFail:
                            quiz_score.total_score = score_total
                            quiz_score.passOrFail = result_model
                            quiz_score.max_score = max_score
                            quiz_score.code = Upload.objects.get(title=in_sys_file)  # f.read()
                            quiz_score.save()
                except ObjectDoesNotExist:
                    quiz_score = QuizScore.objects.create(quizId=quiz,
                                            studentId=User.objects.get(studentId=request.user.studentId),
                                            classroom=quiz.classroom,
                                            total_score=score_total,
                                            passOrFail=result_model,
                                                max_score=max_score,
                                            code= Upload.objects.get(title=in_sys_file) #f.read(),
                                            )
                upload_instance = Upload.objects.get(title=in_sys_file, Uploadfile=in_sys_file ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                if quiz.mode == "Scoring":
                    if score_total == None:
                        score_total = 0
                    upload_instance.score = score_total
                elif quiz.mode == "Pass or Fail":
                    if result_model == None:
                        result_model = 0
                    upload_instance.score = result_model
                upload_instance.save(update_fields=["score"])
                f.close()
                #print(eval('dir()'))
            try:
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result_set,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'Timer':timer_stop.timestamp()*1000,
                                                       'Deadtimestamp':deadline.timestamp()*1000,
                                                       })
            except Exception as e:
                #print(e)
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result_set,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'Timer': False,
                                                       'Deadtimestamp': deadline.timestamp() * 1000,
                                                       })

        elif request.method == 'POST' and 'code-form-submit' in request.POST:
            code = request.POST['code-form-comment']
            code_temp = code
            #print("in-code-form")
            if code == '':
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                        'quizDetail': quiz.quizDetail,
                                                        'Deadline': quiz.deadline,
                                                        'Hint': quiz.hint,
                                                        'code': code,
                                                       'Timer':timer_stop.timestamp()*1000,
                                                   'Deadtimestamp':deadline.timestamp()*1000,
                                                       })
            else:
                rs = get_random_string(length=7)
                fileName = str(request.user.studentId) + '_coded_' + str(quiz.quizTitle) + '_' + str(quiz.classroom.className) + '_' + rs +'.py'
                f = open('./media/' + fileName, 'w')
                for debug_line in code:
                    #print(debug_line)
                    f.write(debug_line)
                f.close()
                Upload.objects.get_or_create(title=fileName, Uploadfile=fileName, user=request.user, quiz=quiz, classroom=quiz.classroom)
                write_mode = False
                test_case_count = 0
                Out_count = 0
                score_total = 0
                max_score = 0
                # open file .txt. Address  file ???????? Now! change follow your PC
                with open('./media/' + fileName, 'r+') as f:
                    code = f.read()
                    f.seek(0, 0)
                    for line in quiz.text_testcase_content.splitlines():
                        if "# Lib" in line:
                            f.write("import ".rstrip('\r\n') + line[6:].rstrip('\r\n') + '\n' + code)
                            break
                try:
                    restricted_globals = dict(__builtins__=safe_builtins)
                    byte_code = compile_restricted(code, filename='./media/' + fileName, mode='exec')
                    exec(byte_code, restricted_globals, {})
                except Exception as E:
                    pass
                if fileName[:-3] in sys.modules:
                    del sys.modules[fileName[:-3]]
                    # importlib.invalidate_caches()
                    prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                else:
                    prob = importlib.import_module(fileName[:-3])
                    # importlib.reload(prob)
                    # print(prob)
                f = open('./media/' + fileName, 'a')
                case = quiz.text_testcase_content
                f.write("\n\n")
                for case_line in case.splitlines():
                    if (case_line[:11] == "# Test case"):
                        test_case_count += 1
                        globals()['case_%s_result' % str(test_case_count)] = ""
                        Out_count += 1
                    f.write(case_line + "\n")
                f.close()
                for i in range(test_case_count):
                    i += 1
                    globals()['test_case_out_%s' % i] = ""
                    globals()['out_%s' % i] = ""
                f = open('./media/' + fileName, 'r')
                code_a = f.read()
                f.close()
                for line in code_a.splitlines():
                    if "# Stop" in line:
                        #print("stop")
                        write_mode = False

                    if write_mode:
                        if "# Out" in line:
                            #print("Out")
                            globals()['out_%s' % test_case_num] = eval(line[6:],{'__builtins__': safe_builtins},{})
                        elif "# Score" in line:
                            #print("SOCREEEE")
                            globals()['score_%s' % test_case_num] = float(eval(line[8:],{'__builtins__': safe_builtins},{}))
                        elif "# Break" in line:
                            #print("Break!")
                            write_mode = False
                        if "prob." in line:
                            command = line
                            # print("command this line")
                            # print(command)
                            '''try:
                                exec_command = inspect.getsource(eval(command[:-4]))
                                byte_code = compile_restricted(exec_command, '<inline>', 'exec')
                                print(byte_code)
                                exec(byte_code, {'__builtins__': utility_builtins}, {})
                            except Exception as E:
                                print(E)
                                continue'''

                        try:
                            globals()['test_case_out_%s' % test_case_num] = eval(command)


                        except Exception as E:
                            print(E)
                            continue

                    if "# Test case" in line:
                        #print("in testcase  ")
                        test_case_num = str(line[11])
                        write_mode = True

                for i in range(test_case_count):
                    i += 1
                    max_score += + globals()['score_%s' % i]
                # unittest process.
                class MyTestCase(unittest.TestCase): pass
                case_result = {}
                for i in range(1, test_case_count + 1, 1):
                    string = "def test_text_{0}(self):\n" \
                             "    self.text_{0} = test_case_out_{0}\n" \
                             "    self.mt_{0} = out_{0}\n" \
                             "    if self.text_{0} == self.mt_{0}:\n" \
                             "        globals()['case_{0}_result'] = 'PASS'\n" \
                             "    else:\n" \
                             "        globals()['case_{0}_result'] = 'FAIL'\n" \
                             "        globals()['score_{0}'] = 0\n" \
                             "    self.assertEquals(self.text_{0}, self.mt_{0})\n".format(i)
                    eval(compile(string, '<string>', 'exec'), globals())
                    setattr(MyTestCase, "test_text_{0}".format(i), str_to_class('test_text_{0}'.format(i)))
                    # from types import MethodType
                    # MyTestCase.test_text_1 = MethodType(test_text_1,MyTestCase)
                    # print(eval("'test_text_{0}'.format(i)"))
                    # method_list = [func for func in dir(MyTestCase) if
                    # callable(getattr(MyTestCase, func)) and not func.startswith("__")]
                    # print(method_list)

                test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
                test_result = TextTestRunner().run(test_suite)
                x = len(test_result.failures)
                for i in range(1, test_case_count + 1, 1):
                    case_result["test_text_{0}".format(i)] = globals()['case_{0}_result'.format(i)]
                if quiz.mode == "Pass or Fail" and x == 0:
                    result = "PASS"
                    result_model = 10
                    max_score = 10
                elif quiz.mode == "Pass or Fail" and x != 0:
                    result = "FAIL"
                    result_model = 0
                    max_score = 10
                elif quiz.mode == "Scoring":
                    for i in range(test_case_count):
                        i += 1
                        score_total = score_total + globals()['score_%s' % i]
                    result = "PASS"
                    result_model = 0
                else:
                    result = "FAIL"
                    result_model = 0
                case_result["result"] = result
                result_set = {'result': case_result,
                              'scoring': {'total_score': score_total, 'max_score': max_score}
                              }
                print(case)
                if QuizStatus.objects.get(quizId=quiz, studentId=User.objects.get(studentId=request.user.studentId),
                                          classroom=quiz.classroom).status == False:
                    QuizTracker.objects.update_or_create(
                        studentId=User.objects.get(studentId=request.user.studentId),
                        classroom=quiz.classroom,
                    )
                    quizDoneCount = QuizTracker.objects.get(studentId=User.objects.get(studentId=request.user.studentId),
                                                            classroom=quiz.classroom, )
                    quizDoneCount.quizDoneCount += 1
                    quizDoneCount.save()
                    quizStatus = QuizStatus.objects.get(quizId=quiz,
                                                        studentId=User.objects.get(studentId=request.user.studentId),
                                                        classroom=quiz.classroom,
                                                        )
                    quizStatus.status = True
                    quizStatus.save()
                #print(str(test_case_count) + ' ' + str(Out_count))
                for i in range(test_case_count):
                    i += 1
                    globals()['test_case_out_%s' % i] = ""
                    globals()['out_%s' % i] = ""
                    globals()['score_%s' % i] = 0
                test_case_count = 0
                Out_count = 0
                with open('./media/' + fileName, 'w') as f:
                    f.write(code_temp)
                f = open('./media/' + fileName, 'r')
                try:
                    quiz_score = QuizScore.objects.get(quizId=quiz,
                                                       studentId=User.objects.get(studentId=request.user.studentId),
                                                       classroom=quiz.classroom)
                    if quiz.mode == "Scoring":
                        if score_total >= quiz_score.total_score:
                            print(str(quiz_score.total_score) + ":" + str(quiz_score.passOrFail))
                            print(str(score_total)+":"+str(result_model))
                            print(fileName)
                            #return None
                            quiz_score.total_score = score_total
                            quiz_score.passOrFail = result_model
                            quiz_score.max_score = max_score
                            quiz_score.code =  Upload.objects.get(title=fileName) #f.read()
                            quiz_score.save()
                    else:
                        if result_model >= quiz_score.passOrFail:
                            quiz_score.total_score = score_total
                            quiz_score.passOrFail = result_model
                            quiz_score.max_score = max_score
                            quiz_score.code = Upload.objects.get(title=fileName)  # f.read()
                            quiz_score.save()
                except ObjectDoesNotExist:
                    quiz_score = QuizScore.objects.create(quizId=quiz,
                                            studentId=User.objects.get(studentId=request.user.studentId),
                                            classroom=quiz.classroom,
                                            total_score=score_total,
                                            passOrFail=result_model,
                                                max_score=max_score,
                                            code= Upload.objects.get(title=fileName) #f.read(),
                                            )
                upload_instance = Upload.objects.get(title=fileName, Uploadfile=fileName ,user=request.user, quiz=quiz, classroom=quiz.classroom)
                if quiz.mode == "Scoring":
                    if score_total == None:
                        score_total = 0
                    upload_instance.score = score_total
                elif quiz.mode == "Pass or Fail":
                    if result_model == None:
                        result_model = 0
                    upload_instance.score = result_model
                upload_instance.save(update_fields=["score"])
                f.close()
                #print(eval('dir()'))
            try:
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result_set,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'Timer':timer_stop.timestamp()*1000,
                                                       'Deadtimestamp':deadline.timestamp()*1000,})
            except Exception as e:
                print(e)
                return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                       'quizDetail': quiz.quizDetail,
                                                       'Deadline': quiz.deadline,
                                                       'Hint': quiz.hint,
                                                       'display': result_set,
                                                       'Case_Count': test_result.testsRun,
                                                       'mode': quiz.mode,
                                                       'code': code_temp,
                                                       'Timer': False,
                                                       'Deadtimestamp': deadline.timestamp() * 1000, })
        else:
            #print("not-in-code-form")
            try:
                Timer = QuizTimer.objects.get(quizId=quiz, studentId=User.objects.get(studentId=request.user.studentId),
                                              classroom=quiz.classroom, )
                if Timer.timer:
                    if not Timer.start:
                        Timer.timer_stop = timezone.now() + timezone.timedelta(seconds=Timer.timer)
                    Timer.start = True
                    Timer.save(update_fields=["timer_stop","start"])
                    return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                           'quizDetail': quiz.quizDetail,
                                                           'Deadline': quiz.deadline,
                                                           'Hint': quiz.hint,
                                                           'Timer': Timer.timer_stop.timestamp() * 1000,
                                                           'code': code_temp,
                                                           'Deadtimestamp': deadline.timestamp() * 1000,
                                                           })

            except ObjectDoesNotExist:
                return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                                   'quizDetail':quiz.quizDetail,
                                                   'Deadline':quiz.deadline,
                                                   'Hint':quiz.hint,
                                                    'Timer':False,
                                                    'code': code_temp,
                                                    'Deadtimestamp':deadline.timestamp()*1000,
                })
    except Exception as e:
        print(e)
        try:
            if request.method == 'POST' and 'upload_submit' in request.POST:
                code_temp = ''
            return render(request, 'Upload.html',{'quizTitle':quiz.quizTitle,
                                                       'quizDetail':quiz.quizDetail,
                                                       'Deadline':quiz.deadline,
                                                       'Hint':quiz.hint,
                                                        'Timer':False,
                                                        'exception':e,
                                                        'code':code_temp,
                                                        'Deadtimestamp':deadline.timestamp()*1000,
                                                  })
        except Exception as e:
            return render(request, 'Upload.html', {'quizTitle': quiz.quizTitle,
                                                   'quizDetail': quiz.quizDetail,
                                                   'Deadline': quiz.deadline,
                                                   'Hint': quiz.hint,
                                                   'Timer': False,
                                                   'exception': e,
                                                   'Deadtimestamp': deadline.timestamp() * 1000,
                                                   })

def moss(request, classroom, quiz_id):
    if request.user.is_admin:
        userid = 367349587
        m = mosspy.Moss(userid, "python")
        for i in QuizScore.objects.filter(quizId__pk=quiz_id):
            try:
                m.addFile(i.code.Uploadfile.path)
            except Exception as E:
                print(E)
                continue
        url = m.send()  # Submission Report URL
        print("Report Url: " + url)
        return redirect(url)
    else:
        return HttpResponseRedirect("/ClassRoom/"+classroom)