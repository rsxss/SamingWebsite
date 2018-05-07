from django.conf.urls import include, url
from . import views

app_name = 'Class_Management'
urlpatterns = [
    #url(r'^$', views.index, name='CLASSROOM'),
    #url(r'^(?P<className>[0-9]+)/$', views.inside, name='Inside'),
    url(r'^(?P<classroom>[\w.@+-]+)/Assignment/', include('Assign_Management.urls')),
    url(r'^$', views.ClassSelect, name='select_class'),
    url(r'^generate_classroom', views.GenerateClassroom, name='GenerateClassroom'),
    url(r'^edit_(?P<classroom>[\w.@+-]+)', views.EditClassroom, name='EditClassroom'),
    url(r'^delete_(?P<classroom>[\w.@+-]+)', views.DeleteClassroom, name='DeleteClassroom'),
    url(r'^(?P<classroom>[\w.@+-]+)/$', views.Home, name='Home'),
    url(r'^(?P<classroom>[\w.@+-]+)/About/$', views.About, name='About'),
    url(r'^(?P<classroom>[\w.@+-]+)/StudentInfo/$', views.StudentInfo, name='StudentInfo'),
    url(r'^(?P<classroom>[\w.@+-]+)/StudentInfo/(?P<username>[\w.@+-]+)/$', views.StudentScoreInfo, name='StudentScoreInfo'),
    url(r'^(?P<classroom>[\w.@+-]+)/StudentInfo/(?P<username>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/$', views.StudentQuizListInfo, name='StudentQuizListInfo'),
    url(r'^(?P<classroom>[\w.@+-]+)/StudentInfo/(?P<username>[\w.@+-]+)/(?P<quiz_id>[0-9]+)/(?P<title>[\w.@+-]+)/$', views.StudentQuizInfo, name='StudentQuizInfo'),
    url(r'^Submit/$', views.Submit, name='SubmitRoom'),
]