from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from accounts.models import User

from .models import *


class RestaurantFeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantFeedback
        fields = (
            'name',
            'overalRate',
            'pros',
            'cons'
        )