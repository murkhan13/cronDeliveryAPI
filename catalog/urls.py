from django.contrib import admin
from django.urls import path
from .views import *
urlpatterns = [
    path('categories/', CategoryListView.as_view()),
    path('dishes/<int:pk>', DishDetailView.as_view()),
    path('dishes/all/', DishSearchView.as_view()),
    path('categories/all/', CategoryItemsSearchView.as_view()),
    path('menu/', MenuPageView.as_view()),
    path('restaurant/', RestaurantView.as_view()),
    path('cart/add/', CartItemAddView.as_view()),
    path('cart/edit/', CartItemEditView.as_view()),
    path('cart/delete/', CartItemDeleteView.as_view())
]