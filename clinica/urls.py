from django.urls import path
from . import views


urlpatterns = [

    path('', views.pagina_inicial, name='pagina_inicial'),
    
    path('clinica/menu', views.menu, name='menu'),
    path('cliente/cadastrar/', views.cadastrar_cliente, name='cadastrar_cliente'),
    path('animal/cadastrar/', views.cadastrar_animal, name='cadastrar_animal'),
    path('veterinario/cadastrar/', views.cadastrar_veterinario, name='cadastrar_veterinario'),
    path('vacina/cadastrar/', views.cadastrar_vacina, name='cadastrar_vacina'),
    path('consulta/cadastrar', views.cadastrar_consulta, name='cadastrar_consulta'),
    path('aplicacao_vacina/cadastrar', views.cadastrar_aplicacao_vacina, name='cadastrar_aplicacao_vacina'),

    path('cadastrar_agendamento', views.cadastrar_agendamento, name='cadastrar_agendamento'),
    
    path('tratamento_realizado/cadastrar', views.cadastrar_tratamento_realizado, name='cadastrar_tratamento_realizado'),

    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('veterinarios/', views.listar_veterinarios, name='listar_veterinarios'),
    path('animais/', views.listar_animais, name='listar_animais'),
    path('vacinas/', views.listar_vacinas, name='listar_vacinas'),
    path('historico/<int:animal_id>/', views.historico_clinico, name='historico_clinico'),
    path('buscar-animal/', views.buscar_animal, name='buscar_animal'),
    # Rota para a tela de agendamentos do dia para visualizacao do funcionario que fara os servicos
    path('agendamentos-do-dia/', views.agendamentos_do_dia, name='agendamentos_do_dia'),
    # Rota para a nova tela de listagem com calendário
    path('listar-agendamentos/', views.listar_agendamentos, name='listar_agendamentos'),


    path('clientes/editar/<int:pk>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/excluir/<int:pk>/', views.excluir_cliente, name='excluir_cliente'),

    path('register/', views.register, name='register'),
    path('logout/', views.custom_logout, name='custom_logout')

]
