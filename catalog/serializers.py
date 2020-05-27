# from django.contrib.auth.models import User
from rest_framework import serializers
from accounts.models import User

from .models import Dish, Category, Restaurant, DishAdditive, DishExtra, Cart, CartItem


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

class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # items = serializers.StringRelatedField(many=True)

    class Meta:
        model = Cart
        fields = (
            'id', 
            'user', 
            'created_at',
            'updated_at', 
            # 'items'
        )

    @staticmethod
    def get_product(obj):
        return obj.dish.title 


class CartItemSerializer(serializers.ModelSerializer):
    cart = CartSerializer(read_only=True)
    dish = DishSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = (
            'id', 
            'cart', 
            'dish', 
            'additives', 
            'extra', 
            'quantity'
        )




class DishListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Dish
        fields = ('id','title', 'image', 'price', 'additives', 'extra')


class DishAdditivesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DishAdditive
        fields = ('id', 'name', 'addPrice', 'active')


class DishExtrasSerializer(serializers.ModelSerializer):
    
    class Meta: 
        model = DishExtra
        fields = ('id', 'name', 'price', 'active')


class CategoriesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ('id','name',)


class DishDetailSerializer(serializers.ModelSerializer):
    #dish_details = DishDetailSerializer(many = True, read_only = True)
    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)
    if extra: 
        pass
    else:
        extra = {"extra": False}

    class Meta: 
        model = Dish
        fields =  ('id', 'title', 'image', 'price',  'portionWeight','description', 'category', 'additives', 'extra')


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
    
    # def to_representation(self, instance):
    #      # instance is the model object. create the custom json format by accessing instance attributes normaly and return it
    #     categories = dict()

    #     representation = {'categories': [instance]  } 

    #     return representation
    
        
    # def to_representation(self, data):
    #     defaultDict = data
    #     ret = []
    #     ret.append({ "categories": [
    #         defaultDict
    #     ]})
    #     return ret
    

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