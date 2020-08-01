
# Create your views here.


from rest_framework.generics import GenericAPIView, RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from django.db.models import Prefetch
from .serializers import *
from .models import *
from django.shortcuts import get_object_or_404
from itertools import chain
from django.db.models import Prefetch, Q, FilteredRelation
from cronProjectAPI.settings import ALLOWED_HOSTS

from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from django.shortcuts import get_object_or_404
from catalog.models import Restaurant
from orders.models import Order

import json
from rest_framework import filters



class RestauranFeedbacksView(APIView):
    """
    A class for representing and adding feedbacks to restaurant

    Args:
        APIView ([class]): [class from rest_framework]
    """

    def get(self, request, *args, **kwargs):
        feedbacks_qs = RestaurantFeedback.objects.filter(restaurant=Restaurant.objects.filter(title=request.data['restaurant'])


    def post(self, request):
        try:
            point   = request.data['point']
            pros    = request.data['pros']
            cons    = request.data['cons']
        except:
            return Response({
                "status": False,
                "detail": "Ошибка при добавлении отзыва"
            }
        feedback = RestaurantFeedback.objects.create(
            name=self.request.user.name,
            overallPoint=point,
            pros=pros,
            cons=cons
        )

