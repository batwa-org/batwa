from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


def one_week_hence():
    return timezone.now() + timezone.timedelta(days=7)


class CustomUser(AbstractUser):
    total_amount = models.FloatField(default=0)
    weekly_limit = models.FloatField(default=0)
    daily_limit = models.FloatField(default=0)
    weekly_limit_reset_date = models.DateTimeField(default=one_week_hence())
    daily_limit_reset_date = models.DateTimeField(default=timezone.now())

    def reset_weekly_limit(self):
        if self.weekly_limit_reset_date < timezone.now():
            self.weekly_limit = 0
            self.weekly_limit_reset_date = one_week_hence()
            self.save()

    def __str__(self):
        return self.username

    class Meta:
        proxy = True


class Category(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    # replace these with unicode emojis?
    # icon = models.ImageField(upload_to='icons/')

    def __str__(self):
        return self.name


# class User(User):
#     id = User.natural_key
#     total_amount = models.FloatField(default=0, null=True)

#     class Meta:
#         proxy = True

#     def __str__(self):
#         return self.username


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
    title = models.CharField(
        max_length=200, default="blank note", blank=False, null=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title
