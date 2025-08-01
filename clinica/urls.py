from django.urls import path
from . import views

urlpatterns = [
    path('clinica/menu', views.menu, name='menu'),
    path('cliente/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('animal/cadastrar/', views.cadastrar_animal, name='cadastrar_animal'),
    path('veterinario/cadastrar/', views.cadastrar_veterinario, name='cadastrar_veterinario'),
    path('vacina/cadastrar/', views.cadastrar_vacina, name='cadastrar_vacina'),
    path('cconsulta/cadastrar', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('aplicacao_vacina/cadastrar', views.cadastrar_aplicacao_vacina, name='cadastrar_aplicacao_vacina'),
    path('agendamento/cadastrar', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    path('tratamento_realizado/cadastrar', views.cadastrar_tratamento_realizado, name='cadastrar_tratamento_realizado'),

    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('veterinarios/', views.listar_veterinarios, name='listar_veterinarios'),
    path('animais/', views.listar_animais, name='listar_animais'),
    path('vacinas/', views.listar_vacinas, name='listar_vacinas'),
    path('historico/<int:animal_id>/', views.historico_clinico, name='historico_clinico'),
    path('buscar-animal/', views.buscar_animal, name='buscar_animal'),

    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),

]
