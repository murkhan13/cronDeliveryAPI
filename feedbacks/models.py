from django.db import models
from catalog.models import Restaurant
from orders.models import Order
from accounts.models import User

# Create your models here.

class Feedback(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.SET_DEFAULT,
        related_name='feedbacks',
        default=None
    )
    order       = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        blank=True,
        null=True
    )
    restaurant  = models.ForeignKey(
        Restaurant,
        on_delete = models.CASCADE,
        related_name='feedbacks', 
        blank=True,
        null=True
    )
    overallRate = models.IntegerField()
    pros        = models.CharField(max_length=255, verbose_name='Плюсы', default='нет')
    cons        = models.CharField(max_length=255, verbose_name='Минусы', default='нет')


class FeedbackImage(models.Model):
    feedback = models.ForeignKey(
        Feedback,
        on_delete=models.CASCADE,
        related_name='images',
        blank=True,
        null=True
    )
    
