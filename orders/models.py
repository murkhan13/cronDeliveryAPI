from django.db import models
from django.contrib.auth import get_user_model
from catalog.models import CartItem
from django.core.validators import RegexValidator


User = get_user_model()


class Address(models.Model):
    user            = models.ForeignKey(
                        User,
                        related_name='adresses',
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,               
    )
    street          = models.CharField(("Улица"),max_length=255)
    building        = models.CharField(("Дом"), max_length=255)
    porch           = models.CharField(("Подъезд"), max_length=255, blank=True,null=True)
    floor           = models.CharField(("Этаж"), max_length=255, blank=True, null=True)
    apartment       = models.CharField(("Квартира"), max_length=255, blank=True, null=True)
    comment         = models.CharField(("Комментарий"),max_length=255, blank=True, null=True)
    created_at      = models.DateTimeField(("Дата создания"), auto_now_add=True)

    class Meta: 
        verbose_name_plural = "Адрес"


class Order(models.Model):

    PAYMENT_CHOICES = (
        (u'H', u'Наличными курьеру'),
        (u'K', u'Оплата картой курьеру'),
        (u'G', u'Оплатить с помощью Google Pay'),
        (u'A', u'Оплатить с помощью Apple Pay')
    )
    ORDER_STATUSES = (
        (u'N', u'Новый'),
        (u'P', u'В Пути'),
        (u'D', u'Доставлен'),
    )

    user            = models.ForeignKey(
                        User,
                        related_name='orders',
                        on_delete=models.CASCADE,
                        null=True,
                        blank=True,               
    )
    phone_regex     = RegexValidator(regex=r'^\+?1?\d{9,20}$',
                        message="Номер телефона должен быть в формате: '+999999999'.Разрешено до 20 символов.")
    phone           = models.CharField(("Номер телефона"), validators = [phone_regex], max_length=20)
    total           = models.DecimalField(("Итоговая сумма"), max_digits=8, decimal_places=2, null=True, blank=True)
    deliverTo       = models.CharField(("Доставить к"), max_length=255)

    address         = models.CharField(("Адрес"), max_length=255)

    personsAmount   = models.IntegerField(("Количество персон"), default=1)
    orderStatus     = models.CharField(("Статус Заказа"), max_length=100, choices=ORDER_STATUSES, default='N')
    paymentMode     = models.CharField(("Способ оплаты"), max_length=100, default='Наличными курьеру')

    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta: 
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return "%s заказал %s" %(self.user, self.created_at)


class OrderItem(models.Model):
    """A model that contains data for an item in an order."""
    order           = models.ForeignKey(
                        Order,
                        related_name='order_items',
                        on_delete=models.CASCADE
                )
    order_dish      = models.ForeignKey(
                        CartItem,
                        on_delete=models.CASCADE
                )
    quantity        = models.PositiveIntegerField(("Количество"),null=True, blank=True)


    class Meta: 
        verbose_name = "Заказанное блюдо"
        verbose_name_plural = "Заказанные блюда"
   
    def __unicode__(self):
        return '%s: %s' % (self.item.title, self.quantity)
    

