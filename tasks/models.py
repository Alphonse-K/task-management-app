from django.db import models
from django.conf import settings

# Create your models here.
class Task(models.Model):

    CHOICES_CATEGORY = [
        ('personal', 'Personal'),
        ('work', 'Work'),
        ('family', 'Family'),
        ('friend', 'Friend')
    ]

    PRIORITY_CATEGORY = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='tasks'
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    due_date = models.DateField()
    category = models.CharField(choices=CHOICES_CATEGORY, max_length=9)
    priority = models.CharField(choices=PRIORITY_CATEGORY, max_length=6)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


