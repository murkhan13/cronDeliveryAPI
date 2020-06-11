# from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import User

from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = User 
        fields = '__all__'
    
    # def restore_object(self, attrs, instance=None):
    #     user = super(AcoountSerializer, self).restore_object(attrs, instance)
    #     return user 


class DishSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Dish
        fields = (
            'id', 
            'title', 
            'price',
            'image', 
            'description', 
            'portionWeight',
            'category', 
        )


class DishAdditivesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DishAdditive
        fields = ('id', 'name', 'addPrice', 'active')


class DishExtrasSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = DishExtra
        fields = ('id', 'name', 'price', 'active')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta: 
        model = User 
        fields = '__all__'


class DishListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dish
        fields = ('id','title', 'image', 'price', 'additives', 'extra')


class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id','name',)


class DishDetailSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)
    

    class Meta: 
        model = Dish
        fields =  ('id', 'title', 'image', 'price',  'portionWeight','description', 'category', 'additives', 'extra')


class CartItemSerializer(serializers.ModelSerializer):

    # dish = DishDetailSerializer(read_only=True)
    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    category    = CategoriesSerializer(many=True, read_only=True)
    additives   = DishAdditivesSerializer(many=True,read_only=True)
    extra       = DishExtrasSerializer(many=True,read_only=True)


    # def to_internal_value(self, data):
    #     cart_data = data['cart']
    #     return super().to_internal_value(cart_data)

    class Meta:
        model = CartItem
        fields = (
            'id', 
            'cart',
            'title', 
            'price',
            'image', 
            'description',
            'portionWeight',
            'category',
            'additives', 
            'extra', 
            'quantity'
        )

    def create(self, validated_data):
        pass


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items')


class DishSearchSerializer(serializers.ModelSerializer):
    
    category = CategoriesSerializer(many=True, read_only=True)
    
    class Meta:
        model = Dish
        fields = ('id', 'title', 'image', 'price',  'category')


class CategoryItemsSerializer(serializers.ModelSerializer):
    
    dishes = DishDetailSerializer(many=True, read_only = True)
    
    class Meta:
        model = Category
        fields =  ['id', 'name', 'dishes']
    

class CategoryItemsSearchSerializer(serializers.ModelSerializer):
    
    dishes = DishDetailSerializer(many=True, read_only = True)
    
    class Meta:
        model = Category
        fields =  ['id', 'name', 'dishes']
    

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Restaurant
        fields = ( 'title', 'workTime', 'minOrder', 'freeOrder', 'address', 'delivery', 'logo', 'info')
    

'''
class DishDetailSerializer(serializers.ModelSerializer):
    
    image_url = serializers.URLField(source='get_absolute_image_url', read_only=True)

    class Meta:
        model = DishDetails
        fields = ('dish', 'image_url')  '''