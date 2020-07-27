from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from accounts.models import User

from .models import *


class FeedbackSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedback
        fields = "__all__"