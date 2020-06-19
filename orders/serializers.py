from catalog.serializers import UserSerializer, CartDishSerializer
from catalog.models import CartItem
from catalog.serializers import CategoriesSerializer, DishAdditivesSerializer, DishExtrasSerializer

from orders.models import *
from rest_framework import serializers


class CartItemToOrderSerializer(serializers.ModelSerializer):

    category = CategoriesSerializer(many=True, read_only=True)
    additives = DishAdditivesSerializer(many=True, read_only=True)
    extra = DishExtrasSerializer(many=True, read_only=True)

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
            'extra'
        )
        
    
    
    # def get_dish_details(self, obj):
        
    #     cartitem = CartItem.objects.filter(cart=obj.cart)
 
    #     return CartDishSerializer(cartitem, many=True).data


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = (
            'id',
            "street", 
            "building",
            "porch",
            "floor",
            "apartment",
            "comment",
            "created_at"
        )


class OrderItemSerializer(serializers.ModelSerializer):
    
    order_dish = CartItemToOrderSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'order_dish',
            'quantity',
        )


class OrderSerializer(serializers.ModelSerializer):

    # user = UserSerializer(read_only=True)
    # address = AddressSerializer(many=True,read_only=True)
    order_items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 
            'user',
            'address',
            'phone',
            'deliverTo',
            'created_at', 
            'order_items',
            'address',
            'created_at',
            'total' 
        )
    
    def create(self, validated_data):
        
        validated_data: dict

        order = Order.objects.create(**validated_data)
        return order