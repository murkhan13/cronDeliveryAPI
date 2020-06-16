from catalog.serializers import UserSerializer, CartDishSerializer
from catalog.models import CartItem

from orders.models import *
from rest_framework import serializers


class CartItemToOrderSerializer(serializers.ModelSerializer):

    dishDetail = serializers.SerializerMethodField('get_dish_details')

    class Meta:
        model = CartItem
        fields = ('dishDetail')
    
    
    def get_dish_details(self, obj):
        
        cartitem = CartItem.objects.filter(cart=obj.cart)
 
        return CartDishSerializer(cartitem, many=True).data


class OrderSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    order_items = serializers.StringRelatedField(many=True, required=False)

    class Meta:
        model = Order
        fields = (
            'id', 
            'user', 
            'total', 
            'created_at', 
            'order_items'
        )
    
    def create(self, validated_data):
        
        validated_data: dict

        order = Order.objects.create(**validated_data)
        return order


class OrderItemSerializer(serializers.ModelSerializer):

    order_dish = CartItemToOrderSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'order_dish',
            'quantity'
        )