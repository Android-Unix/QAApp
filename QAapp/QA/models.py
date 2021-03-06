from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from QAapp.settings import AUTH_USER_MODEL
import uuid

class Question(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    question = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return (self.question + " , marks : " + str(self.marks))


class Answer(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, related_name='answered_users')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='related_question')
    answer = models.TextField()

    def __str__(self):
        return "USERNAME --> " + (str(self.user.username) + " | QUESTION --> " + str(self.question.question) + " | ANSWER --> " + self.answer)


class AssignMarks(models.Model):
    id = models.UUIDField(editable=False, unique=True, primary_key=True, default=uuid.uuid4)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='marks_allocated_answers')
    allocated_marks = models.IntegerField()
    