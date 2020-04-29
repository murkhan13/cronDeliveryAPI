from django.db import models
import os
from django.conf import settings


# Create your models here.


class Category(models.Model):
    # Model representing a dish category
    name = models.CharField(("Название категории"),max_length=200, help_text='Введите категорию блюда(например, супы, салаты, пицца и т.д.')

    def __str__(self):
        # String for representing the Model object.
        return self.name 
    
    def get_category_name(self, obj):

        return obj.name
    
    class Meta:
        verbose_name_plural = "Категории"

from django.urls import reverse


class Dish(models.Model):
    #Model representing a dish to order 
    title = models.CharField(("Навзание блюда"),max_length = 200, help_text='Назовите блюдо')
    price = models.IntegerField(("Цена блюда"),help_text = 'Укажите цену')
    image = models.ImageField(("Картинка блюда"),upload_to="dishes_imgs", default = '002.jpg')
    description = models.CharField(("Описание блюда"),max_length = 200, help_text = 'Опишите блюдо')
    portionWeight = models.IntegerField(("Масса порции"),help_text = "укажите массу порции")
    category = models.ManyToManyField(Category, help_text='Выберите категорию(ии) блюда (для выбора нескольких категорий зажмите клавишу CTRL или Command на MacOS',related_name='dishes')

    class Meta:
        verbose_name_plural = "Блюда"
   
    '''def get_absolute_image_url(self):
        return os.path.join(settings.MEDIA_URL, self.image.url)'''
    def get_image_url(self, obj):
        return obj.image.url 
    
    
    def display_category(self):
        # Creates a string for the Category. This is require to display genre in Admin
        return ', '.join([category.name for category in self.category.all()[:3]])

    display_category.short_description = 'Category'

    def __str__(self):
        # String for representing the Model object.
        return self.title

    def get_absolute_url(self):
        return reverse("dish-detail", args=[str(self.id)])

    def get_image_filename(self, filename):
         id = self.dish.id 
         return "dish_images/%s" % (id)


class DishAdditive(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE,related_name="additives", default='')
    name = models.CharField(("Название добавки"),help_text="укажите название", max_length=200, default = "")
    addPrice = models.IntegerField(("Цена"),help_text="укажите цену")
    active = models.BooleanField(("Добавить"))

    class Meta: 
         verbose_name_plural = "Добавки к блюду"

    def __str__(self):
        return self.name
    

class DishExtra(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="extra", default='')
    name = models.CharField(("Дополнительно"),help_text="укажите дополнительные продукты к блюду",  max_length=200)
    price = models.IntegerField(("Цена"), help_text="укажите цену" )
    active = models.BooleanField("Добавить")

    class Meta:
        verbose_name_plural = "Дополнительно к блюду"


class Restaurant(models.Model):
    #categories = models.ForeignKey(Category, related_name = 'categories', on_delete=models.SET_NULL, null = True)
    title = models.CharField(("Название ресторана"),max_length = 200)
    workTime = models.CharField(("График работы"),max_length = 200, help_text='укажите ') 
    minOrder = models.IntegerField(("Средний чек"),help_text='Минимальный заказ')
    freeOrder = models.IntegerField(("Бесплатная доставка с суммы заказа от:"))
    address = models.CharField(("Адрес ресторана"),max_length = 200)
    delivery = models.IntegerField(("Стоимость доставки"))
    info = models.CharField(("Информация о ресторане"),max_length=200, help_text='Информация')

    class Meta: 
        verbose_name_plural = "Ресторан"

    def __str__(self):
        return self.title


'''

class DishDetails(models.Model):

     dish = models.ForeignKey(Dish, on_delete = models.CASCADE, related_name = 'images')
     images = models.ImageField(upload_to="dishes_imgs")

     def get_absolute_image_url(self):
        return os.path.join(settings.MEDIA_URL, self.images.url)
 '''