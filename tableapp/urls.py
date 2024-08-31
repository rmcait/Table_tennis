from django.contrib import admin
from django.urls import path, include
from .views import indexfunc, employeefunc

urlpatterns = [
    path('index/', indexfunc, name='index'),
        path('employee/', employeefunc, name='employee'),
]
