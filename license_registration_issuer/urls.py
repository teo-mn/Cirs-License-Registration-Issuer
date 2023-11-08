"""
URL configuration for license_registration_issuer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
import json

from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from rest_framework import generics

from license_registration_issuer.views import RegisterView, AddEmployeeView, RemoveEmployeeView, UpdateView


class TestView(generics.GenericAPIView):
    def post(self, request):
        print(json.dumps(request.data))
        return HttpResponse(json.dumps(request.data), headers={"Content-Type": "application/json"})


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register', RegisterView.as_view()),
    path('api/add_employee', AddEmployeeView.as_view()),
    path('api/remove_employee', RemoveEmployeeView.as_view()),
    path('api/update', UpdateView.as_view()),
    path('test', TestView.as_view())
]
