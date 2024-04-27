"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf.urls.static import static
from . import settings
from .settings import PATH_PREFIX

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path(PATH_PREFIX+'admin/', admin.site.urls),
    path(PATH_PREFIX+'user/', include('user.urls')),
    path(PATH_PREFIX+'inventory/', include('inventory.urls')),
    path(PATH_PREFIX+'sentry-debug/', trigger_error),
    path(PATH_PREFIX+'order/', include('order.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)