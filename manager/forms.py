# manager/forms.py
from django import forms
from .models import Task

# manager/forms.py
class TaskForm(forms.ModelForm):
    class Meta:
        model  = Task
        fields = [...]
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
