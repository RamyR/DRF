from django.urls import path
from . import views

urlpatterns = [
    path('application', views.ApplicationMixinView.as_view(), name='application'),
    path('application/<int:pk>', views.ApplicationMixinView.as_view(), name='application-retrieve'),
    path('loan-fund', views.LoanFundMixinView.as_view(), name='loan-fund'),
    path('loan-fund/<int:pk>', views.LoanFundMixinView.as_view(), name='loan-fund-retrieve'),
    path('payment', views.PaymentMixinView.as_view(), name='payment'),
    path('payment/<int:pk>', views.PaymentMixinView.as_view(), name='payment-retrieve'),
    path('user', views.UserMixinView.as_view(), name='user'),
    path('user/<int:pk>', views.UserMixinView.as_view(), name='user-retrieve'),
]