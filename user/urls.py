from django.urls import path, include
from user import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('login-otp/', views.LoginOTPView.as_view(), name='login-otp'),
    path('get-user/', views.GetUserView.as_view(), name='get-user'),
    path('refresh-token/', TokenRefreshView.as_view(), name='refresh-token')
]
