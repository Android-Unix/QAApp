from django.urls import path , include
from . import views

urlpatterns = [
    path('' , views.home , name = 'home'),
    path('signup/' , views.signUP , name = 'signup'),
    path('<uuid:lecturer_id>/students/' , views.list_students , name = 'students'),
    path('<uuid:lecturer_id>/students/filter-based-on-students-answered/' , views.filter_based_on_students_answered, name = 'filtered_students'),
    path('<uuid:lecturer_id>/students/filter-based-on-students-answered/<uuid:student_clicked>/' , views.student_answers, name = 'student_clicked'),
    path('<uuid:lecturer_id>/students/<uuid:student_clicked>/' , views.student_answers , name = 'student_clicked') ,
    path('accounts/' , include('django.contrib.auth.urls')),
    path('addquestion/' , views.addQuestion , name = 'addQuestion'),
    path('restricted/' , views.unauthorisedAccess , name = 'restrict'),
    path('update/<uuid:question_id>/' , views.updateQuestion , name = 'update'),
    path('delete/<uuid:question_id>/' , views.delete_question , name = 'delete'),
    path('answer/<uuid:question_id>/' , views.answerQuestion , name = 'answer'),
    path('<uuid:lecturer_id>/students/<uuid:student_clicked>/allocate-marks/<uuid:answer_clicked>/' , views.allocate_marks, name = 'allocate_marks'),
    path('<uuid:lecturer_id>/students/filter-based-on-students-answered/<uuid:student_clicked>/allocate-marks/<uuid:answer_clicked>/' , views.allocate_marks, name = 'allocate_marks') ,
]
