
from __future__ import unicode_literals
import os
from django.db import models
from django.conf import settings

from django.utils import timezone

from accounts.models import User




class Category(models.Model):
    # Model representing a dish category
    name = models.CharField(("Название категории"),max_length=200, help_text='Введите категорию блюда(например, супы, салаты, пицца и т.д.')
    
    def __str__(self):
        # String for representing the Model object.
        return self.name 
    
    def get_category_name(self, obj):

        return obj.name
    
    class Meta:
        verbose_name = "categories"
        verbose_name_plural = "Категории"

from django.urls import reverse


class Dish(models.Model):
    #Model representing a dish to order 
    title           = models.CharField(("Навзание блюда"),max_length = 200, help_text='Назовите блюдо')
    price           = models.IntegerField(("Цена блюда"),help_text = 'Укажите цену')
    image           = models.ImageField(("Картинка блюда"),upload_to="dishes_imgs", default = '002.jpg')
    description     = models.CharField(("Описание блюда"),max_length = 200, help_text = 'Опишите блюдо')
    portionWeight   = models.IntegerField(("Масса порции"),help_text = "укажите массу порции")
    category        = models.ManyToManyField(Category,
                             help_text='Выберите категорию(ии) блюда (для выбора нескольких категорий зажмите клавишу CTRL или Command на MacOS',related_name='dishes')
    
    
    class Meta:
        verbose_name_plural = "Блюда"
    
    '''def get_absolute_image_url(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)'''
    def get_image_url(self, obj):
        return obj.image.url 
    

    def __str__(self):
        # String for representing the Model object.
        return self.title

    # def get_absolute_url(self):
    #     return reverse("dish-detail", args=[str(self.id)])
    def has_related_object(self):
        has_extra = False
        try:
            has_extra = (self.extra is not None)
        except DishExtra.DoesNotExist:
            pass
        return has_extra and (self.car is not None)

    

class DishAdditive(models.Model):
    dish        = models.ForeignKey(Dish, on_delete=models.CASCADE,related_name="additives", default='')
    name        = models.CharField(("Название добавки"),help_text="укажите название", max_length=200, default = "")
    addPrice    = models.IntegerField(("Цена"),help_text="укажите цену")
    active      = models.BooleanField(("Добавить"))

    class Meta: 
         verbose_name_plural = "Добавки к блюду"

    def __str__(self):
        return self.name
    

class DishExtra(models.Model):
    dish    = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="extra", default='')
    name    = models.CharField(("Дополнительно"),help_text="укажите дополнительные продукты к блюду",  max_length=200)
    price   = models.IntegerField(("Цена"), help_text="укажите цену" )
    active  = models.BooleanField("Добавить")

    class Meta:
        verbose_name_plural = "Дополнительно к блюду"
    
    def __str__(self):
        return self.name



class Restaurant(models.Model):
    #categories = models.ForeignKey(Category, related_name = 'categories', on_delete=models.SET_NULL, null = True)
    title       = models.CharField(("Название ресторана"),max_length = 200)
    workTime    = models.CharField(("График работы"),max_length = 200, help_text='укажите ') 
    minOrder    = models.IntegerField(("Минимальный заказ"),help_text='Минимальный заказ')
    freeOrder   = models.IntegerField(("Бесплатная доставка с суммы заказа от:"))
    address     = models.CharField(("Адрес ресторана"),max_length = 200)
    delivery    = models.IntegerField(("Стоимость доставки"))
    info        = models.CharField(("Информация о ресторане"),max_length=200, help_text='Информация')
    logo        = models.ImageField(("Логотип Ресторана"),upload_to="logos", default = '002.jpg')


    class Meta: 
        verbose_name_plural = "Ресторан"

    def __str__(self):
        return self.title

    def get_image_url(self, obj):
        return obj.logo.url 



class Cart(models.Model):
    user = models.ForeignKey(
        User,
        related_name="cart",
        on_delete=models.CASCADE,
        default=None
        )
    # created_at = models.DateTimeField(editable=False)
    # updated_at = models.DateTimeField()
        
    # def save(self, *args, **kwargs):
    #     ''' On save, update timestamps '''
    #     if not self.id:
    #         self.created_at = timezone.now()
    #     self.updated_at = timezone.now()
    #     return super(Cart, self).save(*args, **kwargs)
    class Meta: 
        verbose_name_plural = "Корзина"


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="items"
    )
    title           = models.CharField(("Навзание блюда"),max_length = 200)
    price           = models.IntegerField(("Цена блюда"))
    image           = models.ImageField(("Картинка блюда"))
    description     = models.CharField(("Описание блюда"),max_length = 200)
    portionWeight   = models.IntegerField(("Масса порции"))
    category        = models.ManyToManyField(Category)

    additives       = models.ManyToManyField(DishAdditive)
    extra           = models.ManyToManyField(DishExtra)

    quantity = models.PositiveIntegerField(default=1)

    def __unicode__(self):
        return '%s: %s' %(self.dish.title, self.quantity)
 