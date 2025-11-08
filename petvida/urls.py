# petvida/urls.py

from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from clinica.views import (
    CustomAuthToken,
    custom_logout,
    agendar_servico,
    get_horarios_disponiveis,
    finalizar_servico,
    save_fcm_token_view,
)
from clinica.views import AgendamentoViewSet, AnimalViewSet, ServicosViewSet

# Roteador para as ViewSets
router = routers.DefaultRouter()
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
router.register(r'animais', AnimalViewSet, basename='animal')
router.register(r'servicos', ServicosViewSet, basename='servico')

# URLs do Django e da sua API
urlpatterns = [
    # URLs da administração e autenticação
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # URLs TRADICIONAIS da sua aplicação web
    path('', include('clinica.urls')),

    # URLs da sua API para o aplicativo Flutter
    path('api/', include(router.urls)),
    
    # Rotas da API que não estão no roteador
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('api/agendar_servico/', agendar_servico, name='agendar_servico'), # <-- Mude o path e o name aqui
    path('api/horarios-disponiveis/', get_horarios_disponiveis, name='horarios_disponiveis'),
    path('api/agendamentos/finalizar/<int:pk>/', finalizar_servico, name='finalizar-servico'),

     # Rota para SALVAR O TOKEN FCM
    path('api/save_fcm_token/', save_fcm_token_view, name='save_fcm_token'),

    
    
]