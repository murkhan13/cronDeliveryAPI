from django.contrib import admin
from .models import Category, Dish, Restaurant, DishAdditive, DishExtra
# Register your models here.
class DishAdditiveInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishAdditive

class DishExtraInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishExtra

class DishInline(admin.TabularInline):
    model = Dish.category.through


class CategoryAdmin(admin.ModelAdmin):
    fk = 'category'
    inlines =[
        DishInline,
    ]


class DishAdmin(admin.ModelAdmin):
    inlines = [DishAdditiveInline, DishExtraInline]

admin.site.register(Dish, DishAdmin)

admin.site.register(Category, CategoryAdmin)
admin.site.register(Restaurant)

#admin.site.register(Dish, ) DishAdmin

'''
class DishDetailsInline(admin.TabularInline):
    fk_name = 'dish'
    model = DishDetails

class ProductAdmin(admin.ModelAdmin):
    inlines = [CategoryInline]
        '''