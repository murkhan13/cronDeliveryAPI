
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('dishes/<int:pk>', DishDetailView.as_view()),
    path('categories/all/', CategoryItemsSearchView.as_view()),
    path('menu/', MenuPageView.as_view()),
    path('cart/add/', CartItemAddView.as_view()),
    path('cart/edit/', CartItemEditView.as_view()),
    path('cart/delete/', CartItemDeleteView.as_view()),
    path('cart/deleteall/', CartDeleteView.as_view())
]