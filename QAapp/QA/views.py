from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .questionform import CreateQuestion , CreateAnswerForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question , Answer

# Create your views here.


def home(request) :
        questions = Question.objects.all()
        return render(request , 'index.html' , {
            'questions' : questions
        })


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

@staff_member_required(login_url='restrict')
def addQuestion(request) :
    if request.method == 'POST' :
        add = CreateQuestion(request.POST)
        if add.is_valid() :
            add.save()
            return render(request , 'success.html' , {
                'tag' : 'Question Added'
            })

    else :
        add = CreateQuestion()

    return render(request , 'QuestionForm.html' , {
        'renderForm' : add
    })

def unauthorisedAccess(request) :
    return render(request , 'alert.html')


@staff_member_required(login_url = 'restrict')
def updateQuestion(request , question_id) :
    question_id = int(question_id)

    try :
        question_selected = Question.objects.get(id = question_id)
    except Question.DoesNotExist:
        return redirect('home')

    UpdateQuestion = CreateQuestion(request.POST or None, instance = question_selected)

    if UpdateQuestion.is_valid():
        UpdateQuestion.save()
        return render(request , 'updatesuccess.html')

    else :
        UpdateQuestion = CreateQuestion(request.POST or None, instance = question_selected)

    return render(request , 'QuestionForm.html' , {
        'renderForm' : UpdateQuestion
    })

def answerQuestion(request , question_id) :
    if request.method == 'POST' :
        form = CreateAnswerForm(request.POST)
        
        if form.is_valid :
            form.save()
            return render(request, 'success.html' , {
                'tag' : 'Answer Submitted!'
            })

    else:
        form = CreateAnswerForm()

    return render(request , 'answerForm.html' , {
        'renderForm' : form
    })
