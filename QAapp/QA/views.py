from django.shortcuts import render, redirect
from account.forms import UserCreationForm, UserLoginForm
from django.http import HttpResponse
from django.contrib.auth.models import User
from .model_form import CreateQuestion, CreateAnswerForm, AssignMarksForm
from django.contrib.admin.views.decorators import staff_member_required
from .models import Question, Answer, AssignMarks
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator
from django.contrib.auth.models import AnonymousUser


User = get_user_model()

def home(request):
    marks_list = list()
    questions = Question.objects.all().order_by('-id')

    if not isinstance(request.user, AnonymousUser):
        marks_list = AssignMarks.objects.filter(answer__user=request.user).order_by('allocated_marks')
        
    if len(marks_list) == 0:
        status = True
    else:
        status = False

    # Show 10 contacts per page.
    paginator = Paginator(questions, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {
        'page_obj': page_obj,
        'number_of_questions': Question.objects.count(),
        'user_uuid': str(request.user.pk),
        'assigned_marks': marks_list,
        'assigned_marks_status': status
    })


def signUP(request):
    if request.method == 'POST' :
        forms = UserCreationForm(request.POST)
       
        if forms.is_valid():
            with open('log.txt', 'w') as file:
                file.write(forms.cleaned_data['first_name'].capitalize())
                file.write('\n')
                file.write(forms.cleaned_data['last_name'].capitalize())
                file.write('\n')
                file.close()

            forms.cleaned_data['first_name'].capitalize()
            forms.cleaned_data['last_name'].capitalize()

            users = forms.save()
            return render(request, 'success.html' , {
                'user_obj': users
            })

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
            return render(request , 'QuestionForm.html' , {
                'question_addition_status' : True
            })
    else :
        add = CreateQuestion()

    return render(request , 'QuestionForm.html' , {
        'renderForm' : add,
        'add_btn': True
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
        return render(request , 'QuestionForm.html', {
            'update_question_status': True
        })

    else :
        UpdateQuestion = CreateQuestion(request.POST or None, instance = question_selected)

    return render(request , 'QuestionForm.html' , {
        'renderForm' : UpdateQuestion,
        'update_btn': True
    })


def answerQuestion(request , question_id):
    question = Question.objects.get(pk=question_id).question
    if request.method == 'POST':
        form = CreateAnswerForm(request.POST)
        if form.is_valid:
            username = request.user.username

            answer = Answer.objects.create(user=User.objects.get(username=username), question=Question.objects.get(pk=question_id), answer=form.data['answer'])
            answer.save()

            return render(request, 'answerForm.html' , {
                'tag' : 'Answer Submitted!',
                'answered': True
            })
    else:
        form = CreateAnswerForm()

    return render(request , 'answerForm.html' , {
        'renderForm' : form,
        'question_name': question
    })


def delete_question(request, question_id):
    question_id = int(question_id)

    try :
        question_selected = Question.objects.get(id = question_id)
        question_selected.delete()

        return render(request, 'deleted_alert.html')

    except Question.DoesNotExist:
        return redirect('home')


def list_students(request, lecturer_id):
    no_students_found = True
    students = []
    is_filtered_list = False

    for user in User.objects.all():
        if not user.is_staff:
            students.append(user)

    if len(students) > 0:
        no_students_found = False

    # Show 10 contacts per page.
    paginator = Paginator(students, 10) 

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'no_students_found': no_students_found,
        'is_filtered_list' : is_filtered_list
    })


def filter_based_on_students_answered(request, lecturer_id):
    filtered_students = []
    no_students_found = True
    is_filtered_list = True

    for user in User.objects.all():
        if not user.is_staff and user.answered_users.count() > 0:
            filtered_students.append(user)

    if len(filtered_students) > 0:
        no_students_found = False

    paginator = Paginator(filtered_students, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'student_list.html', {
        'page_obj': page_obj,
        'no_students_found': no_students_found,
        'is_filtered_list': True
    })
    

def student_answers(request, lecturer_id, student_clicked):
    student = User.objects.get(pk=student_clicked)
    answers_of_student = Answer.objects.filter(user=student)

    return render(request, 'student_answers.html', {
        'answers': answers_of_student,
        'student': student,
        'count': answers_of_student.count(),
        'questions_count': Question.objects.count()
    })


def allocate_marks(request, lecturer_id, student_clicked, answer_clicked):
    clicked_answer = Answer.objects.get(id=answer_clicked)
    errors = set()

    if request.method == 'POST':
        form = AssignMarksForm(request.POST)
        
        if int(form.data['allocated_marks']) >= clicked_answer.question.marks:
            errors.add("Allocated Marks Cannot be More than total marks man!!!")

        if clicked_answer.marks_allocated_answers.count() != 0:
            errors.add("Cannot reassign marks!!!")

        if form.is_valid and int(form.data['allocated_marks']) <= clicked_answer.question.marks and clicked_answer.marks_allocated_answers.count() == 0:
            assigned_marks = AssignMarks.objects.create(answer=clicked_answer, allocated_marks=form.data['allocated_marks'])
            assigned_marks.clean()
            assigned_marks.save()

            return render(request, 'assign_marks.html', {
                'marks_addition_status' : True
            })
    else:
        form = AssignMarksForm()

    return render(request , 'assign_marks.html', {
        'renderForm' : form,
        'errors': errors,
        'add_btn': True
    })