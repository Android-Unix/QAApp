from django.urls import path , include
from . import views


urlpatterns = [
    path('' , views.home , name = 'home') ,
    path('signup/' , views.signUP , name = 'signup') ,
    path('accounts/' , include('django.contrib.auth.urls')) ,
    path('addquestion/' , views.addQuestion , name = 'addQuestion') ,
    path('restricted/' , views.unauthorisedAccess , name = 'restrict') ,
    path('update/<int:question_id>' , views.updateQuestion , name = 'update') ,
]
