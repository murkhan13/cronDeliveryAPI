from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import CartItem
from django.core.validators import RegexValidator


User = get_user_model()


class Order(models.Model):
    user            = models.ForeignKey(
                        User,
                        related_name='orders',
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,               
    )
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                message="Номер телефона должен быть в формате: '+999999999'.Разрешено до 14 цифр.")
    phone           = models.CharField(("Номер телефона"), validators = [phone_regex], max_length=15)
    total           = models.DecimalField(("Итоговая сумма"), max_digits=8, decimal_places=2, null=True, blank=True)
    deliverTo       = models.CharField(("Доставить к"), max_length=255, default="Как можно быстрее")

    #address
    street          = models.CharField(("Улица"),max_length=255)
    building        = models.CharField(("Дом"), max_length=255)
    porch           = models.CharField(("Подъезд"), max_length=255, blank=True,null=True)
    floor           = models.CharField(("Этаж"), max_length=255, blank=True, null=True)
    apartment       = models.CharField(("Квартира"), max_length=255, blank=True, null=True)
    comment         = models.CharField(("Комментарий"),max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(("Дата создания"), auto_now_add=True)


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    order           = models.ForeignKey(
                        Order,
                        related_name='order_items',
                        on_delete=models.CASCADE
                )
    order_dish      = models.ForeignKey(
                        CartItem,
                        related_name='order_items',
                        on_delete=models.CASCADE
                )
    quantity        = models.PositiveIntegerField(("Количество"),null=True, blank=True)
    
    

   
    def __unicode__(self):
        return '%s: %s' % (self.item.title, self.quantity)
    

