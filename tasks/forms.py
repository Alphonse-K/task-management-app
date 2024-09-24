from tasks.models import Task

from django import forms


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'due_date', 'priority', 'category', 'description', 'completed')
        exclude = ('user',)
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Give your task a title'}),
            'due_date': forms.DateInput(attrs={'type': 'date'}),
            'completed': forms.CheckboxInput(),
            'description': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Describe your task - optional'}),
        }
