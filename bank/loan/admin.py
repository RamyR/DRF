import imp
from django.contrib import admin
from .models import User, LoanFund, Application, Payment
# Register your models here.

admin.site.register(User)
admin.site.register(LoanFund)
admin.site.register(Application)
admin.site.register(Payment)
