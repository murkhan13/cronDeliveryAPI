from django.shortcuts import render
from django.db.models import Q , FilteredRelation
from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin 
from .serializers import CategoriesSerializer, CategoryItemsSerializer,CategoryItemsSearchSerializer,  DishSearchSerializer, DishListSerializer
from .serializers import DishDetailSerializer, RestaurantSerializer,DishAdditivesSerializer
from .models import Dish, Category, Restaurant , DishAdditive     #DishDetails
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
import json
from django_filters import rest_framework as rest_filters, NumberFilter, CharFilter
from rest_framework import filters

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


class CategoryListView(ListModelMixin, GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoriesSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, *args, **kwargs):
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


class CategoryFilter(rest_filters.FilterSet):
    dishes = CharFilter(field_name='dishes__title', lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['dishes__title', 'name']



class CategoryItemsSearchView(ListAPIView):
    permission_classes = [AllowAny, ]
    queryset = Category.objects.all()
    serializer_class = CategoryItemsSearchSerializer
    filter_backends = (rest_filters.DjangoFilterBackend, filters.SearchFilter)
    filterset_class = CategoryFilter
    search_fields = ['dishes__title', 'name']

    
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
