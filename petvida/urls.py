
from django.contrib import admin
from django.urls import path, include
from clinica.urls import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.urls')),
]
