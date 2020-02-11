from django.db import models

# Create your models here.

class Question(models.Model) :
    question = models.TextField()
    marks = models.IntegerField()

    def __str__(self):
        return (self.question + " , marks : " + str(self.marks))
