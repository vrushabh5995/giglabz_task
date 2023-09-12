from rest_framework import serializers
from .models import User,Timeconverter



class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True) 
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "mobile", "password"]


class TimeconverterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timeconverter
        fields = '__all__'
