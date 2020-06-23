from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .models import User, PhoneOTP
from .serializers import CreateUserSerializer, UserSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
from rest_framework import status

from django.contrib.auth import login
import random

from knox.views import LoginView as KnoxLoginView
from knox.auth import TokenAuthentication

import requests

def send_sms(phone, key):
    print(phone)
    login = 'CronApp'
    password = 'croncron'
    message = "DeliveryAPPCode:"
    message += str(key) # DeliveryAPPCode:key
    link = "http://smsc.ru/sys/send.php?login=%s&psw=%s&phones=%s&mes=%s" % (login, password, phone, message)
    print(link)

    requests.post(link)

def send_otp(phone):
    if phone:
        key = random.randint(9999, 99999)
        return key
    else:
        return False


class ValidatePhoneSendOTP(APIView):
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)

            if user.exists():
                user_exists = True
            else:
                user_exists = False

            key = send_otp(phone)
            if key:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    old.otp = key
                    count = old.count
                    old.count = count + 1
                    old.save()
                    return Response({
                        "status": True ,
                        "detail": "Номер телефона получен, введите код подтверждения",
                        'key': key,
                        'user_exists': user_exists
                    })
                else:
                    PhoneOTP.objects.create(
                        phone = phone,
                        otp = key
                    )
                        # send_sms(phone, key)
                    return Response({
                        'status': True,
                        "detail": "Номер телефона получен, введите код подтверждения",
                        'key': key,
                        'user_exists': user_exists
                    }) 
            else:
                return Response({
                    'status': False,
                    'detail': 'Ошибка сервера'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Ошибка при отправке номера телефона, попробуйте ещё раз'
            })


class ValidateOtpAndAuthenticate(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format = None):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)
        name = request.data.get('name', False)

        if phone and otp_sent:
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                old = PhoneOTP.objects.filter(phone__iexact = phone)
                if old.exists():
                    old = old.first()
                    otp = old.otp
                    if str(otp_sent) == str(otp):
                        old.validated = True
                        old.save()
                        validated = old.validated
                        if validated:
                            serializer = LoginSerializer(data = request.data)
                            serializer.is_valid(raise_exception=True)
                            user = serializer.validated_data['user']
                            login(request,user)
                            old.delete()
                            print("user:",request.user)
                            return super(ValidateOtpAndAuthenticate, self).post(request, format=None)
                            
                    else: 
                        old.delete()
                        return Response({
                            'status': False,
                            'detail': 'Код подтверждения неверный, повторите попытку'
                        }) 
                else: 
                    return Response({
                        'status': False,
                        'detail': 'Ошибка запроса, сначала отправьте номер телефона'
                    }) 
            else:
                old = PhoneOTP.objects.filter(phone__iexact=phone)
                if old.exists():
                    old = old.first()
                    otp = old.otp
                    if str(otp_sent) == str(otp):
                        old.validated = True
                        old.save()
                        validated = old.validated
                        if validated and name:
                            temp_data = {
                            'name': name,
                            'phone': phone,
                            }
                            serializer = CreateUserSerializer(data=temp_data)
                            serializer.is_valid(raise_exception=True)
                            user = serializer.save()
                            old.delete()
                            serializer = LoginSerializer(data = request.data)
                            serializer.is_valid(raise_exception=True)
                            user = serializer.validated_data['user']
                            login(request,user)
                            print("user:",request.user)
                            return super(ValidateOtpAndAuthenticate, self).post(request, format=None)
                    else: 
                        old.delete()
                        return Response({
                            'status': False,
                            'detail': 'Код подтверждения неверный, повторите попытку'
                        })     
                else: 
                    return Response({
                        'status': False,
                        'detail': 'Ошибка запроса, сначала отправьте номер телефона'
                    })