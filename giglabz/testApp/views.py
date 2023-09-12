from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer,TimeconverterSerializer
from .models import User, Timeconverter
from .authntication import *
from rest_framework.exceptions import APIException
from django.db import connection
import pandas as pd
import pytz
from django.http import JsonResponse
from rest_framework import status
from django.utils import timezone
from datetime import datetime


@csrf_exempt
@api_view(["POST"]) 
def addUser(request):
    if request.method == 'POST':
        serializer =  UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class LoginAPIView(APIView):
    def post(self,request):
        user = User.objects.filter(username = request.data['username'])
        
        if not user:
            raise APIException('Invalid Username!')
        
        
        qry1 = "SELECT * from testApp_user where  username = %s AND password = %s "
        df1 = pd.read_sql(qry1, connection, params=(request.data['username'], request.data['password']))
        
        if df1.empty==False:
            userObj = df1.to_dict('records')[0]

            access_token = create_access_token(userObj['username'])
            
           
            return Response({"token":access_token, "userData":userObj})
        else:
            return Response({"msg":"user not found"})  
        


# to get all user list
class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LogoutAPIView(APIView):
    def post(self,request):
        response=Response()
        response.delete_cookie(key="access_token")
        response.data={'message':'successfully logout'}
        return response



class TimeconverterView(APIView):
    def post(self, request, format=None):
        try:
            input_timezone = request.data.get("timezone")
            input_time = request.data.get("time")

            if not input_timezone or not input_time:
                return Response({"error": "Both timezone and time are required"}, status=status.HTTP_400_BAD_REQUEST)

            input_time = datetime.strptime(input_time, "%Y-%m-%d %H:%M:%S")
            input_time = pytz.timezone(input_timezone).localize(input_time)

            uk_time = input_time.astimezone(pytz.timezone("Europe/London"))
            philippines_time = input_time.astimezone(pytz.timezone("Asia/Manila"))
            us_time = input_time.astimezone(pytz.timezone("America/New_York"))

            data = [

                {"timezone": "UK", "time": uk_time},
                {"timezone": "Philippines", "time": philippines_time},
                {"timezone": "US", "time": us_time},
                {"timezone":input_timezone, "time":input_time}
            ]

            serializer = TimeconverterSerializer(data=data, many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class UpdateUserViewSet(ModelViewSet):
    serializer_class = UserSerializer

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        data=request.data

        instance.username=data.get("username",instance.username)
        instance.first_name=data.get("first_name",instance.first_name)
        instance.last_name=data.get("last_name",instance.last_name)
        instance.email=data.get("email",instance.email)
        instance.mobile=data.get("mobile",instance.mobile)
        instance.password=data.get("password",instance.password)

        instance.save()

        serializer = UserSerializer(instance)

        return Response(serializer.data)



#   to update user by function base view

# @csrf_exempt
# @api_view(["PUT"]) 
# def update(request,username):
#     User= User.objects.get(username=username)
#     auth = authenticate(request)
#     if auth.get("status")==200:
#         serializer=UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)            
#     return Response("Not authorise")






