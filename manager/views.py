from django.contrib.auth import get_user_model, login
from django.db.models import IntegerField, When
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from manager.forms import WorkerCreationForm
from manager.models import *
from urllib.parse import urlencode
from django.views.generic import ListView
from django.db.models import BooleanField, ExpressionWrapper, Q, Case, When, Value, IntegerField
from django.utils import timezone

PRIO_ORDER = {"Urgent": 0, "High": 1, "Normal": 2, "Low": 3}

class HomePageView(ListView, LoginRequiredMixin):
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


class TaskDetailView(DetailView, LoginRequiredMixin):
    model = Task
    context_object_name = "task"
    template_name = "TaskDetails.html"


class TaskListView(ListView, LoginRequiredMixin):
    model = Task
    template_name = "TaskList.html"  # Adjust if your template name is different
    context_object_name = "tasks"    # Optional: customize the variable name in the template
    paginate_by = 10                 # Optional: if you're using pagination

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q')
        if query:
            context['query'] = query
        return context

class TaskCreateView(CreateView, LoginRequiredMixin):
    model = Task
    context_object_name = "task"
    fields = ("name", "description", "task_type", "priority",
              "deadline", "assignees")
    success_url = reverse_lazy("manager:task_list")
    template_name = "TaskCreate.html"


class WorkerListView(ListView, LoginRequiredMixin):
    model = Worker
    context_object_name = "workers"
    template_name = "WorkerList.html"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(position__name__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

class WorkerDetailView(DetailView, LoginRequiredMixin):
    model = Worker
    context_object_name = "worker"
    template_name = "WorkerDetail.html"


class WorkerCreateView(CreateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]  # whatever your form needs
    template_name = "WorkerCreate.html"
    success_url = reverse_lazy("manager:worker_list")

class WorkerDeleteView(DeleteView, LoginRequiredMixin):
    model = Worker
    template_name = "WorkerConfirmDelete.html"
    success_url = reverse_lazy("manager:worker_list")

class TaskCompleteView(View, LoginRequiredMixin):
    def post(self, request, pk):
        Task.objects.filter(pk=pk).update(is_completed=True)
        return redirect("manager:task_details", pk=pk)



User = get_user_model()


class WorkerUpdateView(LoginRequiredMixin, UpdateView):
    model = Worker
    fields = ["username", "first_name", "last_name", "position"]
    template_name = "WorkerUpdate.html"
    success_url = reverse_lazy("manager:worker_list")

class RegisterView(CreateView):
    form_class = WorkerCreationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response