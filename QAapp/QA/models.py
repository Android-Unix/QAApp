from django.db import models

# Create your models here.

class Question(models.Model) :
    question = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return (self.question + " , marks : " + str(self.marks))


class Answer(models.Model) :
    question = models.ForeignKey(Question , on_delete = models.CASCADE)
    answer = models.TextField()

    def __str__(self):
        return (str(self.question) + " , answer : " + self.answer)
