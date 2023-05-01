from django.urls import path
# from .views import Home, PieChartView, DeleteView, CustomLoginView, CategoryList, RegisterPage, TransactionCreate, TransactionDetail, TransactionList, TransactionUpdate, CategoryCreate
from .views import DeleteView, Home, PieChartView, CustomLoginView, RegisterPage, TransactionCreate, TransactionDetail, TransactionList, TransactionUpdate, CategoryCreate, notify_js
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),


    path('', Home.as_view(), name='transactions'),
    path('transaction-list', TransactionList.as_view(), name='transaction-list'),
    path('transaction/<int:pk>/', TransactionDetail.as_view(), name='transaction'),
    path('transaction-create/', TransactionCreate.as_view(),
         name='transaction-create'),
    path('transaction-update/<int:pk>/',
         TransactionUpdate.as_view(), name='transaction-update'),
    path('transaction-delete/<int:pk>/',
         DeleteView.as_view(), name='transaction-delete'),
    path('transaction-delete/<int:pk>/',
         DeleteView.as_view(), name='transaction-delete'),

    path('', TransactionList.as_view(), name='category'),  # why does this exist?
    path('', TransactionList.as_view(), name='category'),  # why does this exist?
    path('category-create/', CategoryCreate.as_view(),
         name='category-create'),
    path('pie_chart/', PieChartView.as_view(), name='pie_chart'),
    path('notify.js', notify_js, name='notify_js'),
]
