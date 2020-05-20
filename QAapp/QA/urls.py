from django.urls import path , include
from . import views


urlpatterns = [
    path('' , views.home , name = 'home') ,
    path('signup/' , views.signUP , name = 'signup') ,
    path('<int:lecturer_id>/students/' , views.list_students , name = 'students') ,
    path('<int:lecturer_id>/students/<int:student_clicked>/' , views.student_answers , name = 'student_clicked') ,
    path('accounts/' , include('django.contrib.auth.urls')) ,
    path('addquestion/' , views.addQuestion , name = 'addQuestion') ,
    path('restricted/' , views.unauthorisedAccess , name = 'restrict') ,
    path('update/<int:question_id>/' , views.updateQuestion , name = 'update') ,
    path('delete/<int:question_id>/' , views.delete_question , name = 'delete') ,
    path('answer/<int:question_id>/' , views.answerQuestion , name = 'answer') ,
]
