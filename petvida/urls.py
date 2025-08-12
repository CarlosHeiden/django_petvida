from django.contrib import admin
from django.urls import path, include
from clinica import views as clinica_views # Importa o seu arquivo de views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('clinica.urls')),
    path('accounts/logout/', clinica_views.custom_logout, name='logout'), # Usa a sua view personalizada
    path('accounts/', include('django.contrib.auth.urls')), # Mantém o restante das views de auth
]