from django.contrib import admin
from django.urls import path
from .views import DishDetailView, CategoryListView, DishSearchView
from .views import  CategoryItemsView, RestaurantView, MenuPageView

urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('dishes/<int:pk>', DishDetailView.as_view()),
    path('dishes/all/', DishSearchView.as_view()),
    path('categories/all/', CategoryItemsView.as_view()),
    path('menu/', MenuPageView.as_view()),
    path('restaurant/', RestaurantView.as_view())
]

