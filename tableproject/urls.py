
from django.contrib import admin
from django.urls import path, include
from tableapp.views import indexfunc


urlpatterns = [
    path('admin/', admin.site.urls),
    path('app/', include('tableapp.urls')),
    path('', indexfunc, name='home'), 
]
