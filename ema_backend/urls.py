"""
URL configuration for ema_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
# myproject/urls.py

from django.contrib import admin
from django.urls import include
from myapp import views, urls
from django.urls import re_path


urlpatterns = [
  re_path('admin/', admin.site.urls),
  re_path('api/auth/', include('dj_rest_auth.urls')),
  re_path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
  re_path('api/', include('myapp.urls')),
]
