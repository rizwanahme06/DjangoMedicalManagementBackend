"""Medical_Store URL Configuration

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
    1. Import to include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from Medical_App import views
from Medical_App.views import CompanyNameViewSet
# import sys

# sys.path.insert(1, "C:\Users\HP\PycharmProjects\Medical_App_folder1\Medical_Store\Medical_App")

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView)

router = routers.DefaultRouter()
# router.register("company", CompanyViewSet, basename="company  ")
router.register("company", views.CompanyViewSet, basename="company")
router.register("companybank", views.CompanyBankViewSet, basename="companybank")
router.register("medicine", views.MedicineViewSet, basename="medicine")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/gettoken/', TokenObtainPairView.as_view(), name="gettoken"),
    path('api/refresh_token/', TokenRefreshView.as_view(), name="refresh_token"),
    path('api/companybyname/<str:name>', CompanyNameViewSet.as_view(), name="companybyname")
]
