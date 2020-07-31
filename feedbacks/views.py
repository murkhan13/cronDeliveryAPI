
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

import json
from rest_framework import filters



class FeedbacksView(APIView):
    """
    A class for representing and adding feedbacks

    Args:
        APIView ([class]): [class from rest_framework]
    """

    def get(self, request, )
