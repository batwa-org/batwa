from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, DeleteView, CustomLoginView, RegisterPage, TransactionCreate, TransactionDetail, TransactionList, TransactionUpdate, CategoryCreate
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterPage.as_view(), name='register'),

    # path('h', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),

    path('', TransactionList.as_view(), name='transactions'),
    path('', TransactionList.as_view(), name='tasks'),
    path('transaction/<int:pk>/', TransactionDetail.as_view(), name='transaction'),
    path('transaction-create/', TransactionCreate.as_view(),
         name='transaction-create'),
    path('transaction-update/<int:pk>/',
         TransactionUpdate.as_view(), name='transaction-update'),
    # path('transaction-delete/<int:pk>/',
    #      DeleteView.as_view(), name='transaction-delete'),

    path('', TransactionList.as_view(), name='category'),
    path('category-create/', CategoryCreate.as_view(),
         name='category-create'),
     #     HERE's some change i made
#     path('notification/')
]
