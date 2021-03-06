from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.http import HttpResponse
from django.template import loader
from django.middleware.csrf import CsrfViewMiddleware
from Class_Management.models import ClassRoom, Quiz
from django.contrib.auth.models import User
import unittest
from unittest import TextTestRunner
from django.conf import settings
from django.core.files.storage import FileSystemStorage

# Create your views here.

def CreateAssignment(request):
    var = request.session['var']
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    else:
        return render(request,'CreateAssignment.html')


def AssignmentDetail(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    return render(request, 'Home.html')


def GenerateAssign(request):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    elif request.method == "POST" and request.FILES['upload_testcase']:
        var = request.session['var']
        Assignment = request.POST.get('Assignment', '')
        Assignment_Detail = request.POST.get('Assignment2', '')
        Deadline = request.POST.get('dateInput','')
        Hint = request.POST.get('hint','')
        dsa = 'upload_testcase' in request.POST and request.POST['upload_testcase']
        asd = request.FILES.get('upload_testcase',False)
        asdf = request.FILES.get('upload_template',False)
        dab = asd.read()
        dabb = asdf.read()
        print(dsa)
        print(dab)
        print(dabb)
        GenerateAssign_instance = Quiz.objects.create(quizTitle=Assignment, quizDetail=Assignment_Detail, deadline=Deadline,text_template_content=dabb ,text_testcase_content=dab  ,hint=Hint,classroom=ClassRoom.objects.get(id=User.objects.get(username=var).extraauth.year))
        #GenerateAssign_instance.save()
        return HttpResponseRedirect('/ClassRoom/Home')
    else:
        return render(request, 'CreateAssignment.html')

def DeleteAssign(request, quiz_id):
    if not request.user.is_authenticated or not request.user.is_superuser:
        return HttpResponseRedirect('/LogOut')
    quiz = Quiz.objects.get(pk=quiz_id)
    quiz.delete()
    return HttpResponseRedirect('/ClassRoom/Home')


def upload(request, quiz_id):
    quiz = Quiz.objects.get(pk=quiz_id)
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/LogOut')
    elif request.method == 'POST' and request.FILES['upload']:
        myfile = request.FILES['upload']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)

        #open file .txt. Address  file ???????? Now! change follow your PC
        f = open('D:/Work/Django_Project/KMUTT_FIBO/241_Grading/SamingDev'+str(uploaded_file_url), 'r')
        code = f.read()
        code = code.lower()
        case = quiz.text_testcase_content
        print(code)
        #unittest process.
        class MyTestCase(unittest.TestCase):
            def test_text(self):
                text = code
                mt = case
                #self.assertEquals(text, "print('hello world')")
                self.assertEquals(text, mt)
            def test_text_two(self):
                text = code
                mt = case
                #self.assertEqual(text, 'print("hello world")')
                self.assertEqual(text,  mt)
        test_suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
        test_result = TextTestRunner().run(test_suite)
        x = len(test_result.failures)
        if x==0:
            result = "PASS"
        else:
            result = "FAIL"

        #sent infomations to page.
        return render(request, 'Upload.html', {
            'quizTitle': quiz.quizTitle,
            'quizDetail': quiz.quizDetail,
            'Deadline': quiz.deadline,
            'Hint': quiz.hint,
            'uploaded_file_url': uploaded_file_url,
            'display': result,
        })
    else:
        return render(request, 'Upload.html', {'quizTitle':quiz.quizTitle,
                                           'quizDetail':quiz.quizDetail,
                                           'Deadline':quiz.deadline,
                                           'Hint':quiz.hint,
        })




