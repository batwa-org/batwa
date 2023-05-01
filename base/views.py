from typing import Any, Dict
from django import http
from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import TemplateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.http import HttpResponse
from django.shortcuts import render

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Case, Sum, When
from django.db import models


from .models import Category, Transaction
from .forms import PositionForm, UserCreateForm


# login
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('transactions')


# sign up
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreateForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('transactions')

    def form_valid(self, form):
        user = form.save()
        if user is not None:  # user successfully created
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):  # since only setting redirect_authenticated_user wasn't working
        if self.request.user.is_authenticated:
            return redirect('transactions')
        return super(RegisterPage, self).get(*args, **kwargs)


# def notify_js(request):
#     with open('./static/base/notify.js', 'r') as f:
#         js = f.read()
#     response = HttpResponse(js, content_type='application/javascript')
#     return response

def transactions_data(request):
    transactions = Transaction.objects.filter(user=request.user).values(
        'category__name').annotate(total=Sum('amount'))

    data = [['Category', 'Amount spent']]
    for transaction in transactions:
        data.append([transaction['category__name'], transaction['total']])

    return JsonResponse(data, safe=False)


class PieChartView(LoginRequiredMixin, TemplateView):
    template_name = 'base/pie_chart.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        labels = []
        data = []

        queryset = Transaction.objects.filter(user=self.request.user).values(
            'category__name').annotate(total=Sum('amount'))
        for entry in queryset:
            labels.append(entry['category__name'])
            data.append(entry['total'])

        context['labels'] = labels
        context['data'] = data

        return context


def notify_js(request):
    return render(request, './static/base/notify.js')


class TransactionList(LoginRequiredMixin, ListView):
    model = Transaction
    context_object_name = 'transactions'
    context_object_name2 = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = context['transactions'].filter(
            user=self.request.user)

        debit_total = context['transactions'].filter(is_debit=True).aggregate(total_debit=Sum(
            'amount', output_field=models.FloatField()))['total_debit'] or 0.0
        credit_total = context['transactions'].filter(is_debit=False).aggregate(total_credit=Sum(
            'amount', output_field=models.FloatField()))['total_credit'] or 0.0
        context['total_amount'] = debit_total - credit_total

        debit_total = context['transactions'].filter(is_debit=True).aggregate(total_debit=Sum(
            'amount', output_field=models.FloatField()))['total_debit'] or 0.0
        credit_total = context['transactions'].filter(is_debit=False).aggregate(total_credit=Sum(
            'amount', output_field=models.FloatField()))['total_credit'] or 0.0
        context['total_amount'] = debit_total - credit_total

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['transactions'] = context['transactions'].filter(
                title__contains=search_input)
        context['categories'] = Category.objects.filter(user=self.request.user)
        context['selected_category'] = self.request.GET.get('category')
        context['search_input'] = search_input

        return context

    # def render_to_response(self, context: Dict[str, Any], **response_kwargs: Any) -> JsonResponse:
    #     if self.request.is_ajax():
    #         return JsonResponse(transactions_data(self.request.user), safe=False)
    #     else:
    #         return super().render_to_response(context, **response_kwargs)

    # queries for filters

    # queries for filters
    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)

        # query for category filter
        selected_category = self.request.GET.get('category')
        if selected_category:
            queryset = queryset.filter(category__name=selected_category)

        # query for is_debit filter
        selected_is_debit = self.request.GET.get('is_debit')
        if selected_is_debit:
            queryset = queryset.filter(is_debit=selected_is_debit)

        # query for sort by deadline
        sort_order = self.request.GET.get('sort_order')
        if sort_order == 'amount_asc':
            queryset = queryset.order_by('amount')
        elif sort_order == 'amount_desc':
            queryset = queryset.order_by('-amount')

        return queryset


class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    context_object_name = 'transactions'
    context_object_name2 = 'categories'
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['transactions'] = context['transactions'].filter(
            user=self.request.user)
        # context['count'] = context['transactions'].filter(
        #     complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['transactions'] = context['transactions'].filter(
                title__contains=search_input)
        context['categories'] = Category.objects.all()
        context['selected_category'] = self.request.GET.get('category')
        context['search_input'] = search_input

        return context

# one specific transaction with all details


class TransactionDetail(LoginRequiredMixin, DetailView):
    model = Transaction
    context_object_name = 'transaction'
    template_name = 'base/transaction.html'


class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name', 'description']
    success_url = reverse_lazy('category')

    def form_valid(self, form):  # modifying default function
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)

    def create_category(request):
        if request.method == 'POST':
            form = CategoryCreate(request.POST)
            if form.is_valid():
                category = form.save(commit=False)
                category.user = request.user
                category.save()
                return redirect('categorys')
        else:
            form = CategoryCreate(initial={'category': Category()})
        return render(request, 'create_category.html', {'form': form})


class TransactionCreate(LoginRequiredMixin, CreateView):
    model = Transaction
    fields = ['amount', 'is_debit', 'category', 'title', 'description']
    success_url = reverse_lazy('transactions')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(
            user=self.request.user)
        return form

    def form_valid(self, form):  # modifying default function
        form.instance.user = self.request.user
        return super(TransactionCreate, self).form_valid(form)

    def create_transaction(request):
        if request.method == 'POST':
            form = TransactionCreate(request.POST)
            if form.is_valid():
                transaction = form.save(commit=False)
                transaction.user = request.user
                transaction.save()
                return redirect('transactions')
        else:
            form = TransactionCreate(initial={'category': Category()})
        return render(request, 'create_transaction.html', {'form': form})

    # def post(self, request, *args, **kwargs):
    #     transactions = Transaction.objects.filter(user=request.user)
    #     total_amount = sum(
    #         t.amount * (-1 if t.is_debit else 1) for t in transactions)
    #     form = self.get_form()
    #     form.instance.user = self.request.user

    #     if form.is_valid():
    #         new_transaction = form.save(commit=False)
    #         if new_transaction.is_debit and new_transaction.amount > total_amount:
    #             messages.error(
    #                 request, "You do not have enough funds for this transaction")
    #             return self.form_invalid(form)
    #         new_transaction.save()
    #         return redirect('transactions')
    #     else:
    #         return super().self.form_invalid(form)


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    model = Transaction
    fields = ['amount', 'is_debit', 'category', 'title', 'description']
    success_url = reverse_lazy('transactions')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['category'].queryset = Category.objects.filter(
            user=self.request.user)
        return form


class Home(LoginRequiredMixin, TemplateView):
    template_name = 'base/home.html'
    model = Transaction
    context_object_name = 'transactions'
    context_object_name2 = 'categories'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context[self.context_object_name] = self.model.objects.filter(
            user=self.request.user)

        debit_total = context[self.context_object_name].filter(is_debit=True).aggregate(total_debit=Sum(
            'amount', output_field=models.FloatField()))['total_debit'] or 0.0
        credit_total = context[self.context_object_name].filter(is_debit=False).aggregate(total_credit=Sum(
            'amount', output_field=models.FloatField()))['total_credit'] or 0.0
        context['total_amount'] = debit_total - credit_total

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context[self.context_object_name] = context[self.context_object_name].filter(
                title__contains=search_input)
        context[self.context_object_name2] = Category.objects.filter(
            user=self.request.user)
        context['selected_category'] = self.request.GET.get('category')
        context['search_input'] = search_input

        return context
# deleting a transaction


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Transaction
    context_object_name = 'transaction'
    success_url = reverse_lazy('transactions')

    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
