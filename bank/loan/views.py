from calendar import month
from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Sum
from rest_framework import generics, mixins, permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import LoanFund, Application, Payment
from dateutil.relativedelta import relativedelta
from .serializers import UserSerializer, ApplicationSerializer, LoanFundSerializer, PaymentSerializer, ApplicationUpdateSerializer
import datetime


# Create your views here.
class UserMixinView(mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser, )

    def get_queryset(self):
        qs = super().get_queryset()
        request = self.request

        if(request.user.is_superuser):
            return qs
        
        return qs.filter(username=request.user) 

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

class ApplicationMixinView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        
        user = request.user
        if not user.is_authenticated:
            return Application.objects.none()
        # # print(request.user)
        return qs.filter(user=request.user)

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            print(request.user)
            
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response({'Bad Request': "Invalid Data..."}, status=status.HTTP_400_BAD_REQUEST)


class ApplicationUpdateView(generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationUpdateSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if(not request.user.is_superuser):
            return Response({"message": "Unauthorized User"}, status=status.HTTP_401_UNAUTHORIZED)

        if serializer.is_valid():
            if(serializer.validated_data["status"] == 'AV'):
                total_funds = Application.objects.filter(status='AV', loan_fund__type='FD').aggregate(Sum('amount'))["amount__sum"]
                total_loans = Application.objects.filter(status='AV', loan_fund__type='LN').aggregate(Sum('amount'))["amount__sum"]


                print(total_funds-total_loans)
                if(serializer.validated_data["amount"] <= (total_funds-total_loans)):
                    serializer.save()
                    return Response({"message": "application updated successfully"}, status=status.HTTP_206_PARTIAL_CONTENT)
                else:
                    return Response({"message": "Sorry, No Sufficient Funds Available"}, status=status.HTTP_409_CONFLICT)

            serializer.save()
            return Response({"message": "application updated successfully"})

        else:
            return Response({"message": "failed", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        
        return Response({"message": "Bad Request"}, status=status.HTTP_400_BAD_REQUEST)

        



class LoanFundMixinView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = LoanFund.objects.all()
    serializer_class = LoanFundSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        if(request.user.groups.filter(name='Loan Customers').exists()):
            return qs.filter(type='LN')
        elif (request.user.groups.filter(name='Loan Providers').exists()):
            return qs.filter(type='FD')
        # user = request.user
        # if not user.is_authenticated:
        #     return Product.objects.none()
        # # print(request.user)
        return qs

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if(not request.user.is_superuser):
            return Response({"message": "Unauthorized User"}, status=status.HTTP_401_UNAUTHORIZED)
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        # serializer.save(user=self.request.user)
        duration_number = serializer.validated_data.get('duration')
        # print(duration_number.total_seconds())
        # duration = relativedelta(months=+duration_number.total_seconds())
        print(serializer.validated_data)
        serializer.save(duration=duration_number)

class PaymentMixinView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.ListModelMixin, generics.GenericAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        request = self.request
        
        user = request.user
        if not user.is_authenticated:
            return Payment.objects.none()
        # # print(request.user)
        return qs.filter(application__user=request.user)

    def get(self, request, *args, **kwargs): #HTTP -> get
        pk = kwargs.get("pk")
        if pk is not None:
            return self.retrieve(request, *args, **kwargs)
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
