from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.mixins import ListModelMixin 
from .serializers import CategoriesSerializer, CategoryItemsSerializer, DishSearchSerializer
from .serializers import DishDetailSerializer, RestaurantSerializer,DishAdditivesSerializer
from .models import Dish, Category, Restaurant , DishAdditive     #DishDetails
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
import json
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

# Create your views here.


class DishDetailView(RetrieveAPIView):
    queryset = Dish.objects.all()
    serializer_class = DishDetailSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    # def get(self, request, *args, **kwargs):
    #     # get objects
    #     dish = Dish.objects.all()
    #     additives = DishAdditive.objects.all()

    #     context = {
    #             "request": request,
    #     }

    #     # get data from serializers
    #     dishes_ser = DishDetailSerializer(dish, many=True, context=context)
    #     additives_ser = DishAdditivesSerializer(additives, many=True, context=context)

    #     # customize the response data
    #     response = dishes_ser.data + additives_ser.data

    #     # return custom representation of data
    #     return Response(response)


class DynamicSearchFilter(SearchFilter):
    def get_search_fields(self, view, request):
        return request.GET.getlist('search_fields', [])


class DishSearchView(ListModelMixin, GenericAPIView):
    queryset =  Dish.objects.all()
    serializer_class = DishSearchSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )
    filter_backends = (SearchFilter,)
    search_fields = ['title','description', 'category__name']
    def get(self, request,*args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryListView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CategoryItemsView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter, DjangoFilterBackend)
    search_fields = ['name', 'dishes__title', 'dishes__description']
    # fiterset_fields = ['dishes__title', 'name']
    filter_fields = ['name','dishes__title']



    def get(self, request,*args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(CategoryItemsView, self).list(request, *args, **kwargs) 

        # customize the response data
        response.data = {"categories": response.data} 
        

        
        # return response with this custom representation
        return response 


class RestaurantView(ListModelMixin, GenericAPIView):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        # call the original 'list' to get the original response
        response = super(RestaurantView, self).list(request, *args, **kwargs) 
        
        # customize the response data
        response.data = {'restaurant': response.data[0:]}
        

        # return response with this custom representation
        return  response


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
