from django.shortcuts import render
from django.db.models import Q , FilteredRelation
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin 
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
# from rest_framework.decorators import detail_route
# from rest_framework.decorators import list_route
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import get_object_or_404

import json
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import filters

# Create your views here.


class DishDetailView(RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

class DynamicSearchFilter(filters.SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class DishSearchView(ListModelMixin, GenericAPIView):
    queryset =  Dish.objects.all()
    serializer_class = DishSearchSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (filters.SearchFilter,)
    search_fields = ['title','description', 'category__name']
    def get(self, request,*args, **kwargs):
        return self.list(request, *args, **kwargs)

# class CustomSearchFilter(SearchFilter):
#     def get_search_fields(self, view, request):
#         if request.get_queryset.get('name','dishes__title'):
#             return ['name', 'dishes__title']
#         return super(CustomSearchFilter, self).get_search_fields(view, request)


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
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    # filterset_class = CategoryFilter
    search_fields = ['name','dishes__title' ]

    
    # def get_queryset(self):

    #     search_term = self.request.GET['search']
        
    #     return Category.objects.filter(
    #         Q(dishes__title__icontains=search_term)
    #     )
    
    # def get(self, request, *args, **kwargs):
    #     search_term = ''
    #     if 'search' in self.request.GET:
    #         print(self.request.GET['search'])
    #         search_term = self.request.GET['search']
    #     categories = Category.objects.filter(dishes__title__icontains=search_term)
    #     serializer = CategoryItemsSearchSerializer(categories, many=True)
    #     category_serializer_data = serializer.data
    #     el = []
    #     for category in category_serializer_data:
    #         elem = category.pop('dishes', None)
        
    #     for dish in range(len(elem)):
    #         if elem[dish]['title'] != search_term and elem[dish]['title'] != search_term.capitalize():
    #             del elem[dish]
    #         elif elem[dish]['title'] == search_term or elem[dish]['title'] == search_term.capitalize():
    #             print(elem[dish])


    #     for category in category_serializer_data:
    #         category['dishes'] = elem
    #     print('\n\n\n',elem)
        
        

    #     return Response(category_serializer_data)
         
    # def get(self, request, *args, **kwargs):
    #     search_term = ''
    #     if 'search' in self.request.GET:
    #         search_term = self.request.GET['search']
    #     categories = Category.objects.filter(dishes__title__icontains=search_term)
    #     # dishes = Dish.objects.filter(title__icontains=search_term)
    #     category_serializer = CategoryItemsSerializer(categories, many=True)
    #     # dishes_serializer = DishListSerializer(dishes, many=True)
    #     category_serializer_data = category_serializer.data
    #     # dishes_serializer_data = dishes_serializer.data

        
       

    #     for category in category_serializer_data:
    #         elem = category.pop('dishes', None)
    #         for dish in range(len(elem)-1): 
    #             if elem[dish]['title'] != search_term :
    #                 del elem[dish]
    #                 print(elem[dish])
                
    #             elif elem[dish]['title'] != search_term or elem[dish]['title'] != search_term.capitalize():
    #                 category['dishes'] = elem[dish]
                
        
    #             # for dishes in category['dishes']:
    #             #     print(dishes)
    #                 # for dish in range(len(dishes)):
    #                 #     print(dish['title'])
    #                 # while count < len(category['dishes']):
                        
    #                 #     print(dishes)
    #                 #     count+=1
    #                     # if dishes[count] != search_term and dishes[count] != search_term.capitalize():
                            
    #                         # if dishes['title'] != search_term and dishes['title'] != search_term:
    #                         #     print(dishes)
                                

    #                          # print(len(category['dishes']) , "\n\n\n")
                            
    #                     # for dishes in category:
    #                     #     for dish in dishes: 
    #                     #         if dish['title'] != search_term:
    #                     #             del dishes[dish]
    #                     # el = category.pop('dishes', None)
    #                     # for dish in range(len(el)-1):
    #                     #     if el[dish]['title'] == search_term and el[dish]['title'] == search_term.capitalize():
    #                     #         category['dishes'] = el[dish]
    #                     #         # print(el[dish])
    #                     #         # del el[dish]
    #                     #     elif el[dish]['title'] != search_term and el[dish]['title'] != search_term.capitalize():
                            
    #                     #         del el[dish]
    #                 # for category2 in category_serializer_data:
    #                 #     category2['dishes'] = dishes_serializer_data
                    


    #     return Response(category_serializer_data) 


class MenuPageView(RestaurantView, CategoryItemsView, ListModelMixin, GenericAPIView):

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
        
        user_cart = Cart.objects.get(user=self.request.user)
        cartitems = CartItem.objects.filter(cart=user_cart)
        serializer = CartItemSerializer(cartitems, many=True)
        return Response(serializer.data)
    
    
    def post(self, request, pk=None):

        try:
            cart = Cart.objects.get(user=self.request.user)
        except:
            cart = Cart.objects.create(id=self.request.user.id,user=self.request.user)
            cart.save()

        try:
            dish = Dish.objects.get(
                pk=request.data['dish_id']
            )
            dish_id = int(request.data.get('dish_id'))
            quantity = int(request.data.get('quantity'))   
            
        except Exception as e:
            return Response({
                'status': False,
                'detail': "Ошибка при добавлении в корзину"
            })
        try: 
            additives = DishAdditive.objects.get(
                id=request.data['additives_id']
            )
        except:
            additives = None
        try: 
            extra_list = request.POST.getlist('extra_id')
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
            except:
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
            extra_list = request.POST.getlist('extra_id')
        except:
            extra_list = None
        
        try:
            cartitem.quantity = quantity
            cartitem.save()
            cartitem.additives.clear()
            cartitem.extra.clear()

            if additives is not None:
                cartitem.additives.add(additives)
            
            if extra_list is not None:
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