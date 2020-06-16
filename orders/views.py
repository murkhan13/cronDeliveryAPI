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

    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)


    def post(self, request, pk=None):

        try: 
            purchaser_id = self.request.user
            purchaser = User.objects.get(id=purchaser_id)
        except :
            raise serializers.ValidationError(
                'Пользователь не найден'
        )

        cart = purchaser.cart 
        

        total_aggregated = cart.items.aggregate(total=Sum())
        total_aggregated_dict = cart.items.aggregate(total=Sum(F('quantity')*F('price'),output_field=FloatField()))


        order_total = round(total_aggregated_dict['total'], 2)
        # order = serializer.save(user=purchaser, total=order_total)
        order = Order(user=purchaser, total=order_total)

        order_items = []

        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, product=cart_item, quantity=cart_item.quantity))
            
        OrderItem.objects.bulk_create(order_items)
        
        cart.items.clear()
