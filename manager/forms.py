# manager/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Task, Worker, Position


# manager/forms.py
class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = "__all__"
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



class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "mt-1 block w-full rounded border-gray-300 shadow-sm",
            "placeholder": "you@example.com",
        }),
    )

    class Meta:
        User = get_user_model()
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # add a common class to all fields
            field.widget.attrs.update({
                "class": "mt-1 block w-full rounded border-gray-300 shadow-sm",
            })


class WorkerCreationForm(UserCreationForm):
    position = forms.ModelChoiceField(
        queryset=Position.objects.all(),
        widget=forms.Select(attrs={
            "class": "mt-1 block w-full rounded border-gray-300 shadow-sm",
        }),
    )

    class Meta:
        model = Worker
        fields = ['username', 'email', 'position', 'password1', 'password2']
