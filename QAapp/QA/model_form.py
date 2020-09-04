from django import forms
from .models import Question, Answer, AssignMarks
from account.models import Account

class CreateQuestion(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

class CreateAnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['answer']


class AssignMarksForm(forms.ModelForm):
    class Meta:
        model = AssignMarks
        fields = ['allocated_marks']
        