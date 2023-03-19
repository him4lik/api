from django.urls import path, include
from user import views

urlpatterns = [
    path('login-otp/', views.LoginOTPView.as_view(), name='login-otp'),
    path('get-user/', views.GetUserView.as_view(), name='get-user'),
]
