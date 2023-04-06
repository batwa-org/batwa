from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    # replace these with unicode emojis?
    # icon = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    complete = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deadline = models.DateTimeField(default=one_week_hence)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'deadline'


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.FloatField(default=0, null=True)
    is_debit = models.BooleanField(default=False, null=True)
    is_credit = models.BooleanField(default=not (is_debit), null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    is_debt = models.BooleanField(default=False, null=True)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.description
