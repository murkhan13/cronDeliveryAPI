from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.conf import settings

User = get_user_model()


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ( 'name', 'phone',)
    
    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = User
        fields = ('id', 'phone', 'name')


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()

    def validate(self, data):

        phone = data.get('phone')

        if phone :
            if User.objects.filter(phone = phone).exists():
                user = User.objects.get(phone = phone)
                print('details:', user.id)
                # user = authenticate( request = self.context.get('request'), phone=phone)
                print("user:",user)
            else:
                msg = {
                    'detail': 'Phone number not found',
                    'status': False
                }
                raise serializers.ValidationError(msg)
            if not user:
                msg = {
                    'detail': 'Phone number and name are not matching, Try again',
                    'status': 'False'
                }
                raise serializers.ValidationError(msg, code= 'authorization')
        else:
            msq = {
                'detail': "Phone number and name weren't found in request",
                'status': False
            }
            raise serializers.ValidationError(msg, code='authorization')
        
        data['user'] = user
        return data


        
    