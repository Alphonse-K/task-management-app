from django.utils import timezone
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.contrib import messages
from tasks.models import Task, Notification
from tasks.forms import TaskForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'
    paginate_by = 3

    
    def get_queryset(self) :
        if self.request.user.is_authenticated:
            queryset = Task.objects.filter(user=self.request.user).order_by('-id')

            # Filter by priority
            priority = self.request.GET.get('priority')
            if priority:
                queryset = queryset.filter(priority=priority)
            
             # Filter by due date
            due_date = self.request.GET.get('due_date')
            if due_date:
                try:
                    # Assuming due_date is in 'YYYY-MM-DD' format
                    due_date = timezone.datetime.strptime(due_date, '%Y-%m-%d').date()
                    queryset = queryset.filter(due_date=due_date)
                except ValueError:
                    pass  # Handle invalid date format as needed
            return queryset
        else:
            return Task.objects.none()     
        
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskForm()
        
        update_forms = [TaskForm(instance=task) for task in context['tasks']]
        context['tasks_with_forms'] = zip(context['tasks'], update_forms) 
        context['notifications'] = Notification.objects.filter(user=self.request.user, is_read=False)
        context['priorities'] = Task.PRIORITY_CATEGORY
        return context
        



class CreateTaskView(LoginRequiredMixin, CreateView):
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, "Task created successfully!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There were errors in the form. Please correct them.")
        return super().form_invalid(form)  # Redirect back to the form with errors
    

class UpdateTaskView(UpdateView):
    model = Task
    template_name = 'tasks/update_task.html'
    form_class = TaskForm
    success_url = reverse_lazy('tasks:home')

    
    def form_valid(self, form):
        form.instance.user = self.request.user
        form.save()
        messages.success(self.request, ("Task successfully updated."))
        return super().form_valid(form)
    
    def form_invalid(self, form):
        messages.error(self.request, ("There were errors in the form, please correct them."))
        return super().form_invalid(form)
    

class TaskDeleteView(DeleteView):
    model = Task
    success_url = reverse_lazy('tasks:home')


    def form_valid(self, form):
        try:
            self.object = self.get_object()
            messages.warning(self.request, ("Task deleted successfully"))
            return super().delete(self.object)
        except Task.DoesNotExist:
            messages.error(self.request, ("Task not found"))
    
    def form_invalid(self, form):
        messages.error(self.request, ("An error occur."))
        return super().form_invalid(form)
    

class MarkNotificationView(View):

    def post(self, request, *args, **kwargs):
        notification_id = kwargs.get('pk')
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
        except Notification.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Notification not found or doesn\'t belong to the user'})

        if not notification.is_read:
            notification.is_read = True
            notification.save()

        return JsonResponse({'status': 'success', 'message': 'Notification marked as read'})        

