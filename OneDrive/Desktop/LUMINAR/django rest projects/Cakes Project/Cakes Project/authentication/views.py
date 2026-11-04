import threading

from django.shortcuts import render
import logging
import smtplib

# Create your views here.
from rest_framework.views import APIView

from django.core.exceptions import ValidationError

from django.contrib.auth import authenticate

from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken

from . serializers import ProfileSerializer

from decouple import config

from cakes.cakes.utils import send_mail

logger = logging.getLogger(__name__)

class LoginView(APIView):

    def post(self,request,*args,**kwargs):

        username = request.data.get('username')

        password = request.data.get('password')

        try:

            if  not username :

                raise ValidationError('must provide username')

            if not password:

                raise ValidationError('must provide password')

        except Exception as e :

            data ={'error':e}

            return Response(data,status=400)

        user = authenticate(username=username,password=password)

        if user :

            refresh_token = RefreshToken.for_user(user)

            access_token = refresh_token.access_token

            data = {'access_token':str(access_token),'refresh_token':str(refresh_token)}

            return Response(data,status=200)

        data = {'msg':'invalid username or password'}

        return Response(data,status=401)

class RegisterView(APIView):

    Serializer_class = ProfileSerializer

    def post(self,request,*args,**kwargs):

        serializer = self.Serializer_class(data=request.data)

        if serializer.is_valid():

            username = serializer.validated_data.get('username')

            profile = serializer.save(email=username)

            recipient = profile.email

            subject ='welcome Abroad Sweet Moments Awaits at cakeTales!'

            template = 'emails/registration.html'

            context = {'name':profile.first_name,'email':recipient,'login_url':config('LOGIN_URL')}

            thread = threading.Thread(
                target=send_mail,
                args=(recipient, subject, template, context),
                daemon=True,
            )
            thread.start()  

            data = {'msg':'user created sucessfully'}

            return Response(data,status=201)

        return Response(serializer.errors,status=400)
