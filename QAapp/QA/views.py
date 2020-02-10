from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .questionform import CreateQuestion

# Create your views here.


def home(request) :
        return render(request , 'index.html')


def signUP(request) :
    if request.method == 'POST' :
        forms = UserCreationForm(request.POST)

        if forms.is_valid() :
            users = forms.save()
            return HttpResponse("SignUp Successful")

    else :
        forms = UserCreationForm()

    return render(request, 'registration/signup.html' , {
        'generateForm' : forms
    })

def addQuestion(request) :
    if request.method == 'POST' :
        add = CreateQuestion(request.POST)
        if add.is_valid() :
            add.save()
            return HttpResponse("Question added successfully")

    else :
        add = CreateQuestion()

    return render(request , 'QuestionForm.html' , {
        'renderForm' : add
    })
