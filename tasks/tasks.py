from celery import shared_task
from celery.schedules import crontab
from config.celery import app
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task, Notification

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync



@shared_task
def send_due_date_notifications():
    # Same logic as before
    tasks = Task.objects.filter(due_date__lte=timezone.now() + timedelta(days=1), completed=False)
    for task in tasks:
        Notification.objects.create(
            user=task.user,
            task=task,
            message=f'Task "{task.title}" is due soon!'
        )
        # print(task.user)
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'notifications_{task.user.id}',
            {
                'type': 'send_notification',
                'notification': {
                    'message': f'Task "{task.title}" is due soon!',
                }
            }
        )


# In your Celery app configuration
app.conf.beat_schedule = {
    'send-due-date-notifications-every-5-minutes': {
        'task': 'tasks.tasks.send_due_date_notifications',
        'schedule': crontab(minute='*/2'),
    },
}
