from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status, generics

from .models import User, PhoneOTP
from .serializers import CreateUserSerializer, UserSerializer, LoginSerializer
from django.shortcuts import get_object_or_404
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

# Create your views here.

class ValidatePhoneSendOTP(APIView):
    
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'phone number already exist'
                })
            else:
                key = send_otp(phone)
                if key:
                    old = PhoneOTP.objects.filter(phone__iexact = phone)
                    if old.exists():
                        old = old.first()
                        old.otp = key
                        count = old.count
                        old.count = count + 1
                        old.save()
                        # send_sms(phone, key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully',
                            'key': key
                        })
                    else:
                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key
                        )
                        # send_sms(phone, key)
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully',
                            'key': key
                        }) 
                else:
                    return Response({
                        'status': False,
                        'detail': 'Sending otp error'
                    })

        else:
            return Response({
                'status': False,
                'detail': 'Phone number is not given in post request'
            })


class AuthValidatePhoneSendOTP(APIView):
    
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone')

        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact = phone)
            if user.exists():
                
                key = send_otp(phone)
                print('key:', key)
                if key:
                    old = PhoneOTP.objects.filter(phone = phone)
                    if old.exists():
                        old = old.first()
                        old.otp = key
                        count = old.count
                        count += 1
                        old.save() 
                        # send_sms(phone, key)  
                        return Response({
                                'status': True,
                                'detail': 'OTP sent successfully',
                                'key': key
                        })    
                         
                    else:
                        PhoneOTP.objects.create(
                            phone = phone,
                            otp = key
                        )
                        return Response({
                            'status': True,
                            'detail': 'OTP sent successfully',
                            'key': key
                        })
                        # send_sms(phone, key)
                else:
                    return Response({
                        'status': False,
                        'detail': 'Sending otp error'
                    })

            else:
                return Response({
                    'status': False,
                    'detail': 'Phone number is not given in post request'
                })
        else: 
            return Response({
                'status': False,
                'detail': 'The User does not exist. Please register first'
            })


def send_otp(phone):
    if phone:
        key = random.randint(9999, 99999)
        return key
    else:
        return False


class ValidateOTP(APIView):

    # If you have received otp, post a request with phone and that ot and you will be redirected to set the password

    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        otp_sent = request.data.get('otp', False)

        if phone and otp_sent:
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                otp = old.otp
                if str(otp_sent) == str(otp):
                    old.validated = True
                    old.save()
                    return Response({
                        'status': True,
                        'detail': 'OTP MATCHED. Please proceed for registration'
                    })
                
                else: 
                    return Response({
                        'status': False,
                        'detail': 'OTP INCORRECT'
                    })
                
            else: 
                return Response({
                    'status': False,
                    'detail': 'First proceed via sending otp request'
                })
        else:
            return Response({
                'status': False,
                'detail': 'Please provide both phone and otp for validation',
            })


class Register(APIView):

    def post(self, request, *args, **kwargs):
        name = request.data.get('name', False)
        phone = request.data.get('phone', False)
        
        if name and phone :
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                validated = old.validated

                if validated:
                    temp_data = {
                        'name': name,
                        'phone': phone,
                    }
                    serializer = CreateUserSerializer(data=temp_data)
                    serializer.is_valid(raise_exception=True)
                    user = serializer.save()
                    old.delete()
                    
                    return Response({
                        'status': True,
                        'detail': 'Account created'
                    })  
        else:
            return Response({
                'status': False,
                'detail': 'Both phone and name are not sent'
            })


class Authenticate(APIView):
    
    def post(self, request, *args, **kwargs):
        phone = request.data.get('phone', False)
        name = request.data.get('name', False)
        if name and phone :
            old = PhoneOTP.objects.filter(phone__iexact = phone)
            if old.exists():
                old = old.first()
                validated = old.validated
                if validated:
                    old.delete()
                    return Response({
                        'status': True,
                        'detail': 'Logged in.'
                    })     
        else: 
            return Response({
                'status': False,
                'detail': 'Both phone and name are not sent'
            })


class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format = None):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request,user)
        print("user:",request.user)
        return super().post(request, format=None)