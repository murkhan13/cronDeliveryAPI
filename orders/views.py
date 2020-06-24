from __future__ import unicode_literals


from django.shortcuts import render
from django.db.models import FloatField
from django.db.models import F
from django.db.models import Sum

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
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
        
        
        if 'deliverTo' in request.data: 
            deliverTo = request.data['deliverTo']
        else: 
            deliverTo = 'Как можно быстрее'
        order = Order(
            user=purchaser, 
            phone=request.data['phone'], 
            total=request.data['total'],
            deliverTo=deliverTo,
            address = request.data['address']
            )

        order.save()

        order_items = []

        
        for cart_item in cart.items.all():
            order_items.append(OrderItem(order=order, order_dish=cart_item, quantity=cart_item.quantity,))

        OrderItem.objects.bulk_create(order_items)
        
        cart.items.clear()

        user_order = Order.objects.filter(id=order.id)

        serializer = OrderSerializer(user_order, many=True)

        return Response(serializer.data)


class OrderSingleView(RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class AddressView(APIView):

    serializer_class = AddressSerializer
    qyeryset = Order.objects.all()
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk=None):

        try:
            user_addresses = Address.objects.filter(user=self.request.user)

            serializer = AddressSerializer(user_addresses, many=True)
            return Response(serializer.data)
        except:
            return Response({
                "status": False
            })

    def post(self, request, pk=None):

        try: 
            street = request.data['street']
            building = request.data['building']
        except:
            return Response({
                "status": False
            })
        if 'porch' in request.data:
            porch = request.data['porch']
        else:
            porch = None
        if 'floor' in request.data:
            floor = request.data['floor']
        else:
            floor = None 
        if 'apartment' in request.data:
            apartment = request.data['apartment']
        else: 
            apartment = None
        if 'comment' in request.data:
            comment = request.data['comment']
        else:
            comment = None

        try:
            new_address = Address.objects.create(
                user=self.request.user,
                street=street,
                building=building,
                porch=porch,
                floor=floor,
                apartment=apartment,
                comment=comment
            )
            return Response({
                "status": True
            })
        except:
            return Response({
                "status": False
            })


class UserProfileView(APIView):

    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get(self, request, pk=None):
        user = self.request.user

        user_queryset = User.objects.filter(pk=user.id)

        serializer = UserProfileSerializer(user_queryset, many=True)

        return Response(serializer.data)

        