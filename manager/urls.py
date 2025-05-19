from django.urls import path
from .views import HomePageView, TaskDetailView, TaskListView, TaskCreateView, WorkerListView, WorkerDetailView, \
    WorkerDeleteView, WorkerCreateView, TaskCompleteView

app_name = "manager"

urlpatterns = [

    path("", HomePageView.as_view(), name="index"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_details"),
    path("task/", TaskListView.as_view(), name="task_list"),
    path("task/create/", TaskCreateView.as_view(), name="task_create"),
    path("worker/", WorkerListView.as_view(), name="worker_list"),
    path("worker/<int:pk>/", WorkerDetailView.as_view(), name="worker_detail"),
    path("worker/<int:pk>/delete/", WorkerDeleteView.as_view(), name="worker_delete"),
    path("worker/create/", WorkerCreateView.as_view(), name="worker_create"),
    path('task/<int:pk>/complete/', TaskCompleteView.as_view(), name='task_complete'),



]
