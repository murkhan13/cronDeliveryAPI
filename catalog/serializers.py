# from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from accounts.models import User


from .models import *


class UserSerializer(serializers.HyperlinkedModelSerializer):

    class Meta: 
        model = User 
        fields = '__all__'
    

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


class CartDishSerializer(serializers.ModelSerializer):

    image = serializers.ImageField(max_length=None, use_url=True, allow_null=True, required=False)
    category    = CategoriesSerializer(many=True, read_only=True)
    additives   = DishAdditivesSerializer(many=True,read_only=True)
    extra       = DishExtrasSerializer(many=True,read_only=True)
    
    class Meta:
        model = CartItem
        fields = (
            'id', 
            'title', 
            'price',
            'image', 
            'description',
            'portionWeight',
            'category',
            'additives', 
            'extra', 
        )


        def to_internal_value(self, data):
            validated = {
            "dishDetail":{
                "id": data.get("id"),
                "title": data.get("title"),
                "price": data.get("price"),
                "image": data.get("image"),
                "description": data.get("description"),
                "portionWeight": data.get("portionWeight"),
                "category": data.get("category"),
                "addtitives": data.get("additives"),
                "extra": data.get("extra")
            },
            "quantity": data.get("quantity")
        }
            return validated


class CartDishQuantity(serializers.ModelSerializer):

    class Meta:
        model = CartItem
        fields = ('id', 'quantity')

    

class CartItemSerializer(serializers.ModelSerializer):
    
    # dishDetail = CartDishSerializer(read_only=True)
    dishDetail = serializers.SerializerMethodField('get_dish_details')
    

    class Meta:
        model = CartItem
        fields = (
            'dishDetail', 
            'quantity'
        )


    def get_dish_details(self, obj):
        
        cartitem = CartItem.objects.filter(cart=obj.cart)
 
        return CartDishSerializer(cartitem, many=True).data

    '''def to_representation(self, instance):
        return {
            'dishDetail': {
                'id': instance.id,
                'title': instance.title,
                'price': instance.price,
                'image': instance.image.url,
                'description': instance.description,
                'portionWeight': instance.portionWeight,
                'category': instance.category,
                'additives': instance.additives,
                'extra': instance.extra
            },
            'quantity': instance.quantity
        }'''
    


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True,read_only=True)

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

