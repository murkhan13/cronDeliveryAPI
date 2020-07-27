from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import  status, generics

from knox.auth import TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated


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
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone')
        

        if phone:
            phone = str(phone)
            user = User.objects.filter(phone__iexact=phone)
            print(phone)
            print(phone)

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
                    send_sms(phone, key)
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
                    send_sms(phone, key)
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
    permission_classes = (AllowAny,)

    def post(self, request, format = None):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)
        # name = request.data.get('name', False)

        if phone and otp_sent:
            phone = str(phone)
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
                    print(old.otp, otp)
                    if str(otp_sent) == str(otp):
                        old.validated = True
                        old.save()
                        validated = old.validated
                        if validated :
                            temp_data = {
                            # 'name': name,
                            'phone': phone,
                            }
                            user = User.objects.create(phone=phone)
                            user.save()
                            # serializer = CreateUserSerializer(data=temp_data)
                            # serializer.is_valid(raise_exception=True)
                            # user = serializer.save()
                            old.delete()
                            serializer = LoginSerializer(data = request.data)
                            serializer.is_valid(raise_exception=True)
                            user = serializer.validated_data['user']
                            login(request,user)

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

class SetUserName(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        user_name = request.data.get('name', False)
        if user_name:
            user = self.request.user
            user.name = user_name
            user.save()
            return Response({
                'status': True,
                'detail': 'Имя пользователя получено'
            })
        else:
            return Response({
                'status': False,
                'detail': 'Имя не отправлено!!!'
            })

class SetUserName(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        user_name = request.data.get('name', False)
        if user_name:
            user = self.request.user
            user.name = user_name
            user.save()
            return Response({
                'status': True,
                'detail': 'Имя пользователя получено'
            })
        else:
            return Response({
                'status': False,
                'detail': 'Имя не отправлено!!!'
            })

class ChangePhone(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def post(self,request):
        user_phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)
        if user_phone:
            phone_toSMS = user_phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')
            phone = str(user_phone)
            old = PhoneOTP.objects.filter(phone__iexact = phone_toSMS)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    user = self.request.user
                    user.phone = phone
                    user.save()
                    old.delete()
                    return Response({
                        "status": True,
                        "detail": "Номер телефона изменён"
                    })         
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
            return Response({
                'status': False,
                'detail': 'Номер телефона не отправлен'
            })

class LogoutView(APIView):

    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication,)

    def post(self, request):
        
        request._auth.delete()
        return Response({
                "success": True
            })
