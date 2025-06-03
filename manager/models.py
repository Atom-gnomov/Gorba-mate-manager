from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class TaskType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,   # keep the row if the position is deleted
        null=True,                   # <— DB may store NULL
        blank=True,                  # <— form may leave it empty
    )

    def __str__(self):
        return self.get_full_name() or self.username



class Task(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    deadline = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    PRIORITY_TYPE = (
        ("Urgent", "Urgent"),
        ("High",   "High"),
        ("Normal", "Normal"),
        ("Low",    "Low"),
    )
    priority = models.CharField(max_length=10, choices=PRIORITY_TYPE)
    task_type = models.ForeignKey(TaskType, on_delete=models.CASCADE)
    assignees = models.ManyToManyField(
        Worker,
        related_name="tasks",
        blank=True
    )
