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

    order_items = OrderItemSerializer(many=True,read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 
            'user',
            'phone',
            'personsAmount', 
            'orderStatus',
            'paymentMode',
            'order_items',

            'address',
            'deliverTo',
            'created_at', 
            
        )
    
    def create(self, validated_data):
        
        validated_data: dict

        order = Order.objects.create(**validated_data)
        return order


class UserProfileSerializer(serializers.ModelSerializer):
    adresses = AddressSerializer(many=True, read_only=True)
    orders = OrderSerializer(many=True, read_only=True)

    class Meta: 
        model = User
        fields = ('id', 'phone', 'name', 'adresses', 'orders')