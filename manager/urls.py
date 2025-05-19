from django.urls import path
from .views import HomePageView, TaskDetailView, TaskListView

app_name = "manager"

urlpatterns = [

    path("", HomePageView.as_view(), name="index"),
    path("task/<int:pk>/", TaskDetailView.as_view(), name="task_details"),
    path("task/", TaskListView.as_view(), name="task_list"),

]
