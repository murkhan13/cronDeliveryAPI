from __future__ import unicode_literals


from django.shortcuts import render
from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from knox.auth import TokenAuthentication

from catalog.models import Cart, CartItem

from .models import *
from .serializers import *



class OrderView(APIView):

    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    
    def get(self, request, pk=None):

        user_orders = Order.objects.filter(user=self.request.user)

        serializer = OrderSerializer(user_orders, many=True)
        return Response(serializer.data)


    def post(self, request, pk=None):


        try: 
            purchaser_id = self.request.user.id
            purchaser = User.objects.get(id=purchaser_id)
            cart = Cart.objects.get(user=purchaser)
        except :
            raise serializers.ValidationError(
                'Пользователь не найден'
        )   
            

        print(cart.items.all())
        
        # cartitems = CartItem.objects.all()

        # serializer = CartItemToOrderSerializer(cartitems, many=True)
        # return Response(serializer.data)

        

        
        # total_aggregated_dict = cart.items.aggregate(total=Sum(F('quantity')*F('price'),output_field=FloatField()))

        # order_total = round(total_aggregated_dict['total'], 2)
        # order = serializer.save(user=purchaser, total=order_total)
        order = Order(user=purchaser, phone=request.data['phone'], total=request.data['total'])

        order.save()

        order_items = []

        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, order_dish=cart_item, quantity=cart_item.quantity,))

        OrderItem.objects.bulk_create(order_items)
        
        cart.items.clear()

        Address.objects.create(
            user=self.request.user, 
            order=order, 
            street=request.data['street'], 
            building=request.data['building']
        )

        user_order = Order.objects.filter(id=order.id)

        serializer = OrderSerializer(user_order, many=True)

        return Response({"order":serializer.data})
