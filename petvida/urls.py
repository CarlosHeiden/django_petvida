from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from clinica.views import AgendamentoViewSet, AnimalViewSet, ServicosViewSet, CustomAuthToken, custom_logout, get_agendamentos_json, finalizar_servico

# Crie um roteador para as ViewSets
router = routers.DefaultRouter()
router.register(r'agendamentos', AgendamentoViewSet, basename='agendamento')
router.register(r'animais', AnimalViewSet, basename='animal')
router.register(r'servicos', ServicosViewSet, basename='servico')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    # Inclua as rotas do roteador da API no caminho 'api/'
    path('api/', include(router.urls)),
    
    # Rota para o login
    path('api/login/', CustomAuthToken.as_view(), name='api_login'),
    path('agendamentos-do-dia-json/', get_agendamentos_json, name='agendamentos_do_dia_json'),

    # Rota para finalizar o serviço e avisar o cliente
     path('api/agendamentos/finalizar/<int:pk>/', finalizar_servico, name='finalizar-servico'),

    
    
    # Rota para as URLs padrão do Django Auth
    path('accounts/logout/', custom_logout, name='logout'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    path('', include('clinica.urls')),
]
