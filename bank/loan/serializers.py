from dataclasses import Field, fields
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import User, LoanFund, Application, Payment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'