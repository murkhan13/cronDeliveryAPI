
from django.contrib import admin
from django.urls import path
from .views import *


urlpatterns = [
    path('orders/', OrderView.as_view()),
]