from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import User, LoanFund, Application, Payment
from .serializers import UserSerializer

# Create your views here.

 