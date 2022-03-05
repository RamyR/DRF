from dataclasses import Field, fields
from tkinter import INSERT
from rest_framework import serializers
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import LoanFund, Application, Payment
from django.contrib.auth.models import User
import datetime

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class LoanFundSerializer(serializers.ModelSerializer):
    type=serializers.CharField(source='get_type_display')
    class Meta:
        model = LoanFund
        fields = '__all__'
    
    def validate(self, data):
        if(data['min_amount'] > data['max_amount']):
            raise serializers.ValidationError({"min_amount":"Min amount must be smaller than or equal to max amount"})
        return data

class ApplicationUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ['user', 'loan_fund']


    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.start_date = datetime.now()
        instance.save()
        return instance

class ApplicationOfPaymentSerializer(serializers.ModelSerializer):
    loan_fund_details = LoanFundSerializer(source='loan_fund' ,read_only=True)
    status = serializers.CharField(source='get_status_display')
    class Meta:
        model = Application
        fields = ['id', 'start_date', 'loan_fund', 'status', 'amount', 'user', 'loan_fund_details']

class PaymentSerializer(serializers.ModelSerializer):
    application_details = ApplicationOfPaymentSerializer(source='application', read_only=True)
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'date', 'application', 'application_details']

    def create(self, validated_data):
        return super().create(validated_data)

class PaymentForApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    loan_fund_details = LoanFundSerializer(source='loan_fund' ,read_only=True)
    payment_details = PaymentForApplicationSerializer(source='payments', many=True, read_only=True)
    status = serializers.CharField(source='get_status_display', read_only=True)
    class Meta:
        model = Application
        fields = ['id', 'start_date', 'loan_fund', 'user', 'status', 'amount', 'loan_fund_details', 'payment_details']
    
    

    

