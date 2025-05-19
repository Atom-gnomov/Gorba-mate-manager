from django.db.models import IntegerField, When
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from manager.models import *
from urllib.parse import urlencode
from django.views.generic import ListView
from django.db.models import BooleanField, ExpressionWrapper, Q, Case, When, Value, IntegerField
from django.utils import timezone

PRIO_ORDER = {"Urgent": 0, "High": 1, "Normal": 2, "Low": 3}

class HomePageView(ListView):
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


class TaskDetailView(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "TaskDetails.html"


class TaskListView(ListView):
    model = Task
    context_object_name = "tasks"
    template_name = "TaskList.html"
    paginate_by = 10

class TaskCreateView(CreateView):
    model = Task
    context_object_name = "task"
    fields = ("name", "description", "task_type", "priority",
              "deadline", "assignees")
    success_url = reverse_lazy("manager:task_list")
    template_name = "TaskCreate.html"


class WorkerListView(ListView):
    model = Worker
    context_object_name = "workers"
    template_name = "WorkerList.html"


class WorkerDetailView(DetailView):
    model = Worker
    context_object_name = "worker"
    template_name = "WorkerDetail.html"


class WorkerCreateView(CreateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]  # whatever your form needs
    template_name = "WorkerCreate.html"
    success_url = reverse_lazy("manager:worker_list")

class WorkerDeleteView(DeleteView):
    model = Worker
    template_name = "WorkerConfirmDelete.html"
    success_url = reverse_lazy("manager:worker_list")



