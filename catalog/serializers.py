from rest_framework import serializers
from .models import Dish, Category, Restaurant, DishAdditive, DishExtra


class DishListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = ('id','title', 'image', 'price')



class DishAdditivesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = DishAdditive
        fields = ('name', 'addPrice', 'active')


class DishExtrasSerializer(serializers.ModelSerializer):
    class Meta: 
        model = DishExtra
        fields = ('name', 'price', 'active')

class CategoriesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name',)


class DishDetailSerializer(serializers.ModelSerializer):
    #dish_details = DishDetailSerializer(many = True, read_only = True)
    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)

    class Meta: 
        model = Dish
        fields =  ('id', 'title', 'image', 'price',  'portionWeight','description', 'category', 'additives', 'extra')

class DishSearchSerializer(serializers.ModelSerializer):
    category = CategoriesSerializer(many=True, read_only=True)
    class Meta:
        model = Dish
        fields = ('id', 'title', 'image', 'price',  'category')
    
class CategoryItemsSerializer(serializers.ModelSerializer):
    
    dishes = DishListSerializer(many=True, read_only = True)
    
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
    
    dishes = DishListSerializer(many=True, read_only = True)
    
    class Meta:
        model = Category
        fields =  ['id', 'name', 'dishes']
    # def to_representation(self, data):
    #     data = data.filter(dishes__title__icontains=self.context['request'].search, edition__hide=False)
    #     return super(CategoryItemsSearchSerializer, self).to_representation(data)


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