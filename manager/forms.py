# manager/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, Position


# manager/forms.py
class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = '__all__'
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }),
            "description": forms.Textarea(attrs={
                "rows": 3,
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }),
            # keep your flatpickr-ready deadline widget ↓
            "deadline": forms.TextInput(attrs={
                "id": "id_deadline",
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm",
                "autocomplete": "off",
            }),
            "priority": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }),
            "task_type": forms.Select(attrs={
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }),
            "assignees": forms.SelectMultiple(attrs={
                "class": "mt-1 block w-full rounded-lg border-gray-300 shadow-sm "
                         "focus:ring-indigo-500 focus:border-indigo-500 text-sm"
            }),
        }



Worker = get_user_model()

class WorkerCreationForm(UserCreationForm):
    class Meta:
        model = Worker
        fields = (
            'username',
            'password1',
            'password2',
            'first_name',
            'last_name',
            'email',
        )



class CustomRegisterForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        label="Виберіть посаду",  # Ukrainian for "Choose position"
        required=True
    )

    class Meta:
        model = Worker
        fields = ['username', 'email', 'password1', 'password2', 'position']