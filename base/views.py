from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib import messages

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task, Category
from .forms import PositionForm, UserCreateForm


# login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


# sign up
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:  # user successfully created
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):  # since only setting redirect_authenticated_user wasn't working
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    

# main page with todo list, search and filters
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'
    context_object_name2 = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search_input'] = search_input
        context['selected_complete'] = self.request.GET.get('complete')
        context['order_by_deadline'] = self.request.GET.get('deadline')

        return context
    
    # queries for filters
    def get_queryset(self):
        queryset = super().get_queryset()

        # query for category filter
        selected_category = self.request.GET.get('category')
        if selected_category:
            queryset = queryset.filter(category__name=selected_category)

        # query for completeness filter
        selected_complete = self.request.GET.get('complete')
        if selected_complete:
            queryset = queryset.filter(complete=selected_complete)
        
        # query for sort by deadline 
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'deadline_asc':
            queryset = queryset.order_by('deadline')
        elif sort_order == 'deadline_desc':
            queryset = queryset.order_by('-deadline')

        return queryset

# one specific task with all details
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


# creating new task
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'category', 'description', 'deadline', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):  # modifying default function
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)

    def create_task(request):
        if request.method == 'POST':
            form = TaskCreate(request.POST)
            if form.is_valid():
                task = form.save(commit=False)
                task.user = request.user
                task.save()
                return redirect('tasks')
        else:
            form = TaskCreate(initial={'category': Category()})
        return render(request, 'create_task.html', {'form': form})


# updating an existing task
class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'category', 'description', 'deadline', 'complete']
    success_url = reverse_lazy('tasks')


# deleting a task
class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)