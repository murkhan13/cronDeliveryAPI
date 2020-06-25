from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from django.db.models import Prefetch
from rest_framework.mixins import ListModelMixin 
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from itertools import chain
from django.db.models import Prefetch, Q, FilteredRelation

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import get_object_or_404

import json
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import filters


class DishDetailView(RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class CategoryItemsView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request,*args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryItemsSearchView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSearchSerializer 
    # filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    # search_fields = ['dishes__title']
    

    def get(self, request, *args, **kwargs):
        if 'search' in self.request.GET:
            search_term = self.request.GET['search']    
        
        category_name = []
        categoriees = Category.objects.filter(dishes__title__icontains=search_term)
        for i in range(len(categoriees)):
            category_name.append(categoriees[i])


        # filtering given categories query for particular dishes, 
        # and exclude categories with other names 
        
        categories = Category.objects.prefetch_related(
            Prefetch('dishes', queryset=Dish.objects.filter(title__icontains=search_term), to_attr='filtered_dishes')
        ).filter(name__in=category_name)

        serializer = CategoryItemsSearchSerializer(categories, many=True, context={'request': request})

        return Response(serializer.data)
 


class MenuPageView(ListModelMixin, GenericAPIView):

    permission_classes = (IsAuthenticatedOrReadOnly, )
    serializer_class = CategoryItemsView.serializer_class
    

    def get(self, request, *args, **kwargs):
        # get objects
        categories = Category.objects.all()
        restaurant = Restaurant.objects.all()

        context = {
                "request": request,
        }

        # get data from serializers
        categories_serializer = CategoryItemsSerializer(categories, many=True, context=context)
        restaurant_serializer = RestaurantSerializer(restaurant, many=True, context=context)

        # customize the response data
        response = {"categories":categories_serializer.data, "restaurant": restaurant_serializer.data[-1]}

        # return custom representation of data
        return Response(response)


class CartItemAddView(APIView):
    serializer_class = CartSerializer
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)


    def get(self, request):

        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            cart = Cart.objects.create(user=self.request.user)
            cart.save()
        context = {
                "request": request,
        }
        user_cart = Cart.objects.get(user=self.request.user)
        cartitems = CartItem.objects.filter(cart=user_cart)
        serializer = CartItemSerializer(cartitems, many=True, context=context)
        return Response(serializer.data)
    
    
    def post(self, request, pk=None):

        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            cart = Cart.objects.create(id=self.request.user.id,user=self.request.user)
            cart.save()

        try:
            dish = Dish.objects.get(
                pk=int(request.data['dish_id'])
            )
            quantity = int(request.data.get('quantity'))   
            
        except Exception as e:
            return Response({
                'status': False,
                'detail': "Ошибка при добавлении в корзину"
            })
        try: 
            additives = DishAdditive.objects.get(
                id=int(request.data['additives_id'])
            )
        except:
            additives = None
        try:
            extra_list = request.data.get('extra_id')
        except:
            extra_list = None
        # extra_list = [int(s) for s in extra_id.split(',')]

        existing_cart_items = CartItem.objects.filter(cart=cart.id, title=dish.title)

        if additives is not None and extra_list is not None:
            flag = False
            for existing_cart_item in existing_cart_items:
                flag = False 
                if len(existing_cart_item.additives.all()) == 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) > 0:
                    addtv = existing_cart_item.additives.filter(name=additives)
                    if len(addtv) > 0:
                        flag = True
                    if flag:
                        if len(extra_list) != len(existing_cart_item.extra.all()):
                            flag = False
                            continue
                        else:
                            check = 0
                            for extr in extra_list:
                                flag = False
                                extra = existing_cart_item.extra.filter(id=extr)
                                if extra:
                                    check += 1
                            if check == len(existing_cart_item.extra.all()):
                                flag=True
                if flag == True: 
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break
                            
        
        if additives is None and extra_list is not None:
            flag = False
            for existing_cart_item in existing_cart_items:
                flag = False
                if len(existing_cart_item.additives.all()) > 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) == 0:
                    if len(extra_list) != len(existing_cart_item.extra.all()):
                            flag = False
                    else:
                        check = 0
                        for extr in extra_list:
                            flag = False
                            extra = existing_cart_item.extra.filter(id=extr)
                            if extra:
                                check += 1
                        if check == len(existing_cart_item.extra.all()):
                            flag=True
                if flag == True: 
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break
        
        if additives is not None and extra_list is None:
            flag = False
            for existing_cart_item in existing_cart_items: 
                if len(existing_cart_item.additives.all()) == 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) > 0:
                    addtv = existing_cart_item.additives.filter(name=additives)
                    if len(addtv) > 0:
                        flag = True
                    if flag:
                        if len(extra_list) != len(existing_cart_item.extra.all()):
                            flag = False
                            continue
                        if len(existing_cart_item.extra.all()) == 0:
                            flag = True
                if flag == True: 
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break            
        
        if additives is None and extra_list is None:
            flag = False
            for existing_cart_item in existing_cart_items:
                if len(existing_cart_item.additives.all()) > 0:
                    flag = False
                elif len(existing_cart_item.additives.all()) == 0:
                    if len(existing_cart_item.extra.all()) > 0:
                        flag = False
                    elif len(existing_cart_item.extra.all()) == 0:
                        flag = True
                
                if flag == True: 
                    existing_cart_item.quantity += quantity
                    existing_cart_item.save()
                    return Response({
                        "status": True
                    })
                    break

        if flag == False:
            try: 
                '''domain = Site.objects.get_current().domain
                obj = dish
                path = obj.get_image_url()
                image_url = 'https://{domain}{path}'.format(domain=domain, path=path)'''

                new_cart_item = CartItem.objects.create( 
                        cart=cart,
                        title=dish.title,
                        price=dish.price,
                        image=dish.image,
                        description=dish.description,
                        portionWeight=dish.portionWeight,
                        quantity = quantity
                )
                new_cart_item.save()
                category = dish.category
                for cat in category.values():
                    obj = Category.objects.get(name=cat["name"])
                    new_cart_item.category.add(obj)

                if additives is not None:
                    new_cart_item.additives.add(additives)
            
                if extra_list is not None:
                    for extra in extra_list:
                        obj = DishExtra.objects.get(pk=extra)
                        new_cart_item.extra.add(obj)
                return Response({
                        "status": True
                })
            except  Exception as e:
                print(e)
                return Response({
                    "status": False
                }) 
             
class CartItemEditView(APIView):

    def post(self,request,pk=None):

        try:
            cartitem = CartItem.objects.get(
                pk=request.data['cartitem_id']
            )
            quantity = int(request.data['quantity'])
        except Exception as e:
            print(e)
            return Response({
                'status': False ,
                'detail': "Ошибка запроса при изменении товаров в корзине"
            })

        try: 
            additives = DishAdditive.objects.get(
                id=request.data['additives_id']
            )
        except:
            additives = None
        try:
            extra_list = request.data.get('extra_id')
        except:
            extra_list = None        
        try:
            cartitem.quantity = quantity
            cartitem.save()

            if additives is not None:
                cartitem.additives.clear()
                cartitem.additives.add(additives)
            
            if extra_list is not None:
                cartitem.extra.clear()
                for extra in extra_list:
                    obj = DishExtra.objects.get(pk=extra)
                    cartitem.extra.add(obj)
            return Response({
                "status": True
            })
        except:
            return Response({
                "status": False
            })


class CartItemDeleteView(APIView):

    def post(self, request, pk=None):

        try:
            cartitem = CartItem.objects.get(
                pk=request.data['cartitem_id']
            )
        except:
            return Response({
                "status": False,
                "detail": "Товар по такому id не найден"
            })
        try:
            cartitem.delete()
            return Response({
                "status": True
            })
        except:
            
            return Response({
                "status": False
            })


class CartDeleteView(APIView):
    def post(self, request,pk=None):

        try:
            user_cart = Cart.objects.get(user=self.request.user)

            CartItem.objects.filter(cart=user_cart).delete()

            return Response({
                "status": True
            })
        except Exception :
            return ({
                "status": False
            })