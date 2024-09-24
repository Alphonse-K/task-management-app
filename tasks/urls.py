from django.urls import path

from tasks.views import TaskListView, CreateTaskView, UpdateTaskView, TaskDeleteView, MarkNotificationView

app_name = 'tasks'

urlpatterns = [
    path('', TaskListView.as_view(), name='home'),
    path('task/create/', CreateTaskView.as_view(), name='create'),
    path('task/update/<int:pk>/', UpdateTaskView.as_view(), name='update'),
    path('task/delete/<int:pk>/', TaskDeleteView.as_view(), name='delete'),
    path('notifications/mark-as-read/<int:pk>/', MarkNotificationView.as_view(), name='mark_as_read'),
]
