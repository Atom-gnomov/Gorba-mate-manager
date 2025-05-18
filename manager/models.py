from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)


class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)


class Worker(AbstractUser):
    position =  models.ForeignKey(Position,on_delete=models.CASCADE)

class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField()
    priority =