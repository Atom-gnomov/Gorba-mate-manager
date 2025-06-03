from django.contrib.auth import get_user_model, login
from django.db.models import IntegerField, When
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, FormView, UpdateView

from manager.forms import WorkerCreationForm, CustomRegisterForm
from manager.models import *
from urllib.parse import urlencode
from django.views.generic import ListView
from django.db.models import BooleanField, ExpressionWrapper, Q, Case, When, Value, IntegerField
from django.utils import timezone

PRIO_ORDER = {"Urgent": 0, "High": 1, "Normal": 2, "Low": 3}

class HomePageView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "main.html"
    paginate_by = 6

    def get_queryset(self):
        qs = (
            super().get_queryset()
            .filter(is_completed=False)
            .annotate(
                is_expired=ExpressionWrapper(
                    Q(deadline__lt=timezone.now()),
                    output_field=BooleanField(),
                )
            )
        )

        sort_priority  = self.request.GET.get("sort_priority")
        sort_deadline  = self.request.GET.get("sort_deadline")

        if sort_priority:
            qs = qs.annotate(
                prio_order=Case(
                    When(priority="Urgent", then=Value(0)),
                    When(priority="High",   then=Value(1)),
                    When(priority="Normal", then=Value(2)),
                    When(priority="Low",    then=Value(3)),
                    output_field=IntegerField(),
                )
            )
        ordering = []
        if sort_priority:
            ordering.append("prio_order")
        if sort_deadline:
            ordering.append("deadline")
        if ordering:
            qs = qs.order_by(*ordering)

        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)

        params = self.request.GET.copy()
        params.pop("page", None)  # прибираємо номер сторінки
        qs_preserve = params.urlencode()  # sort_priority=1&sort_deadline=1

        # «?sort_priority=1&sort_deadline=1&»  або просто «?»
        base_qs = "?" + (qs_preserve + "&" if qs_preserve else "")
        ctx["base_qs"] = base_qs
        return ctx





class TaskDetailView(LoginRequiredMixin,DetailView):
    model = Task
    context_object_name = "task"
    template_name = "TaskDetails.html"


class TaskListView(LoginRequiredMixin,ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "TaskList.html"
    paginate_by = 10

class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    context_object_name = "task"
    fields = ("name", "description", "task_type", "priority",
              "deadline", "assignees")
    success_url = reverse_lazy("manager:task_list")
    template_name = "TaskCreate.html"


class WorkerListView(LoginRequiredMixin,ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "WorkerList.html"


class WorkerDetailView(LoginRequiredMixin,DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "WorkerDetail.html"


class WorkerCreateView(LoginRequiredMixin,CreateView):
    form_class = WorkerCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class WorkerDeleteView(LoginRequiredMixin,DeleteView):
    model = Worker
    template_name = "WorkerConfirmDelete.html"
    success_url = reverse_lazy("manager:worker_list")

class TaskCompleteView(LoginRequiredMixin,View):
    def post(self, request, pk):
        # does a single SQL UPDATE and touches no other columns
        Task.objects.filter(pk=pk).update(is_completed=True)
        return redirect("manager:task_details", pk=pk)



class RegisterView(FormView):
    template_name = "registration/register.html"
    form_class    = CustomRegisterForm
    success_url   = reverse_lazy("login")

    def form_valid(self, form):
        form.save()                       # form already handles position
        return super().form_valid(form)


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    """
    Lets a logged-in user (or an admin) edit an existing Worker row.
    Reuses Django’s generic UpdateView so only the diff hits the DB.
    """
    model = Worker

    # Fields you actually want editable:
    fields = (
        "first_name",
        "last_name",
        "position",
        "email",
        "username",
    )

    template_name = "WorkerUpdate.html"      # create this file if it doesn't exist
    success_url = reverse_lazy("manager:worker_list")