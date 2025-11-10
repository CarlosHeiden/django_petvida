from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,  get_object_or_404
from django.db.models import Q 
from django.http import JsonResponse
from .models import Cliente, Veterinario, Animal, Vacina, Consulta,Tratamento, AplicacaoVacina, RealizacaoTratamento, Veterinario, Agendamento, Servicos
from .forms import CadastroForm, ClienteForm, AnimalForm, VeterinarioForm, VacinaForm,  AplicacaoVacinaForm, AgendamentoForm, ConsultaForm, RealizacaoTratamentoForm
from datetime import datetime, timedelta, time, date

from .utils import send_push_notification 

from rest_framework.decorators import api_view, permission_classes
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .api.serializers import AgendamentoSerializer,AnimalSerializer, ServicosSerializer


def register(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login') # Redireciona para a página de login após o cadastro
    else:
        form = CadastroForm()
    return render(request, 'registration/register.html', {'form': form})

def pagina_inicial(request):
    """View para a página inicial institucional."""
    return render(request, 'index.html')

@login_required
def menu(request):
    return render(request, 'menu.html')

@login_required
def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = ClienteForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Cliente'})

@login_required
def cadastrar_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = AnimalForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Animal'})

@login_required
def cadastrar_veterinario(request):
    if request.method == 'POST':
        form = VeterinarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = VeterinarioForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Veterinário'})

@login_required
def cadastrar_vacina(request):
    if request.method == 'POST':
        form = VacinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = VacinaForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Vacina'})

# LISTAGENS
def listar_clientes(request):
    termo = request.GET.get('q')
    if termo:
        clientes = Cliente.objects.filter(nome_completo__icontains=termo)
    else:
        clientes = Cliente.objects.all()
    return render(request, 'listar_clientes.html', {'clientes': clientes})

def listar_veterinarios(request):
    termo = request.GET.get('q')
    if termo:
        veterinarios = Veterinario.objects.filter(nome__icontains=termo)
    else:
        veterinarios = Veterinario.objects.all()
    return render(request, 'listar_veterinarios.html', {'veterinarios': veterinarios})

def listar_animais(request):
    termo = request.GET.get('q')
    if termo:
        animais = Animal.objects.select_related('id_cliente').filter(
            Q(nome__icontains=termo) |
            Q(id_cliente__nome_completo__icontains=termo)
        )
    else:
        animais = Animal.objects.select_related('id_cliente').all()
    return render(request, 'listar_animais.html', {'animais': animais})

def listar_vacinas(request):
    termo = request.GET.get('q')
    if termo:
        vacinas = Vacina.objects.filter(
            Q(nome_vacina__icontains=termo) |
            Q(tipo_vacina__icontains=termo)
        )
    else:
        vacinas = Vacina.objects.all()
    return render(request, 'listar_vacinas.html', {'vacinas': vacinas})

def buscar_animal(request):
    animais = Animal.objects.select_related('id_cliente').all()
    return render(request, 'buscar_animal.html', {'animais': animais})


# HISTÓRICO CLÍNICO DE UM ANIMAL
@login_required
def historico_clinico(request, animal_id):
    animal = get_object_or_404(Animal, pk=animal_id)
    tutor = animal.id_cliente

    # Consultas
    consultas = Consulta.objects.filter(id_animal=animal.id).values('data_consulta', 'descricao')

    # Vacinas aplicadas
    vacinas = AplicacaoVacina.objects.filter(id_animal=animal.id).select_related('id_vacina').values('data_aplicacao', 'id_vacina__nome_vacina')

    # Tratamentos realizados
    tratamentos = RealizacaoTratamento.objects.filter(id_animal=animal.id).select_related('id_tratamento').values('data_realizacao', 'observacoes', 'id_tratamento__nome_tratamento')

    # Construir histórico unificado
    historico = []

    for item in consultas:
        historico.append({
            'data': item['data_consulta'],
            'tipo': 'Consulta',
            'descricao': item['descricao']
        })

    for item in vacinas:
        historico.append({
            'data': item['data_aplicacao'],
            'tipo': 'Vacina',
            'descricao': f"Aplicação da vacina: {item['id_vacina__nome_vacina']}"
        })

    for item in tratamentos:
        historico.append({
            'data': item['data_realizacao'],
            'tipo': 'Tratamento',
            'descricao': f"{item['id_tratamento__nome_tratamento']}: {item['observacoes']}"
        })

    # Ordenar histórico por data decrescente
    historico.sort(key=lambda x: x['data'], reverse=True)

    return render(request, 'historico_clinico.html', {
        'animal': animal,
        'tutor': tutor,
        'historico': historico
    })

# CONSULTAS
@login_required
def cadastrar_consulta(request):
    if request.method == 'POST':
        form = ConsultaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = ConsultaForm()
    return render(request, 'formulario.html', {
        'form': form,
        'titulo': 'Cadastrar Consulta'
    })

# APLICAÇÃO DE VACINAS
@login_required
def cadastrar_aplicacao_vacina(request):
    if request.method == 'POST':
        form = AplicacaoVacinaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = AplicacaoVacinaForm()
    return render(request, 'formulario.html', {
        'form': form,
        'titulo': 'Aplicar Vacina'
    })

# AGENDAMENTO
def encontrar_proximo_horario_disponivel(data, duracao, agendamentos_existentes):
    """Encontra o próximo horário disponível no dia para um determinado serviço."""
    
    horario_inicio_dia = time(8, 0) # 8:00 AM
    horario_fim_dia = time(18, 0)  # 6:00 PM
    incremento_minutos = 15
    
    DURACAO_SERVICOS = {
        'Banho': 60,
        'Tosa': 60,
        'Banho e Tosa': 120,
    }
    
    intervalos_ocupados = []
    horario_fim_ultimo = datetime.combine(data, horario_inicio_dia)

    for agendamento in agendamentos_existentes:
        inicio = datetime.combine(data, agendamento.hora_agendamento)
        duracao_existente = DURACAO_SERVICOS.get(agendamento.tipo_servico, 60)
        fim = inicio + timedelta(minutes=duracao_existente)
        intervalos_ocupados.append({'inicio': inicio, 'fim': fim})
        
        if fim > horario_fim_ultimo:
            horario_fim_ultimo = fim

    # CORREÇÃO: Inicia a busca a partir do fim do último agendamento
    horario_atual = horario_fim_ultimo
    
    # Arredonda o horário de início da busca para o próximo incremento
    minuto_atual = horario_atual.minute
    minutos_para_proximo_incremento = (incremento_minutos - (minuto_atual % incremento_minutos)) % incremento_minutos
    horario_atual += timedelta(minutes=minutos_para_proximo_incremento)

    while horario_atual.time() < horario_fim_dia:
        horario_fim_novo = horario_atual + timedelta(minutes=duracao)
        
        if horario_fim_novo.time() > horario_fim_dia:
            break

        conflito = False
        for intervalo in intervalos_ocupados:
            if not (horario_fim_novo <= intervalo['inicio'] or horario_atual >= intervalo['fim']):
                conflito = True
                break
        
        if not conflito:
            return horario_atual.time()
            
        horario_atual += timedelta(minutes=incremento_minutos)
        
    return None

# A função AGORA ACEITA DOIS NOVOS PARÂMETROS COM VALOR PADRÃO
@login_required
def cadastrar_agendamento(request, data=None, hora=None):
    titulo = 'Agendar Serviço'
    
    # 1. LÓGICA POST (SALVAR FORMULÁRIO) - Permanece a mesma
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'Serviço agendado com sucesso!')
            # Retorna para o menu ou para a tela de agendamento rápido
            return redirect('agendar_servico_rapido') 
        else:
            messages.error(request, 'Erro no formulário. Por favor, verifique os campos.')
            
    # 2. LÓGICA GET (EXIBIR FORMULÁRIO)
    else:
        initial_data = {}
        
        # Se a data e hora vieram da URL, pré-popula o formulário
        if data and hora:
            try:
                data_obj = datetime.strptime(data, '%Y-%m-%d').date()
                hora_obj = datetime.strptime(hora, '%H:%M').time()
                
                initial_data['data_agendamento'] = data_obj
                initial_data['hora_agendamento'] = hora_obj
                
                messages.info(request, f"Preencha os detalhes para {data_obj.strftime('%d/%m/%Y')} às {hora_obj.strftime('%H:%M')}")
                
            except ValueError:
                pass # Ignora se a URL vier mal formatada

        form = AgendamentoForm(initial=initial_data)

    return render(request, 'cadastrar_agendamento.html', {'form': form, 'titulo': titulo})

@login_required
def cadastrar_tratamento_realizado(request):
    if request.method == 'POST':
        form = RealizacaoTratamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = RealizacaoTratamentoForm()
    return render(request, 'formulario.html', {
        'form': form,
        'titulo': 'Registrar Tratamento Realizado'
    })

# EDIÇÃO E EXCLUSÃO DE CLIENTES
@login_required
def editar_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)

    return render(request, 'formulario_edicao.html', {
        'form': form,
        'titulo': 'Editar Cliente',
        'botao': 'Salvar Alterações',
        'voltar_url': 'listar_clientes'
    })

@login_required
def excluir_cliente(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)

    if request.method == 'POST':
        cliente.delete()
        return redirect('listar_clientes')

    return render(request, 'confirmar_exclusao.html', {
        'objeto': cliente,
        'tipo': 'Cliente',
        'voltar_url': 'listar_clientes'
    })

@login_required
def custom_logout(request):
    logout(request)
    return render(request, 'registration/logged_out.html')

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        try:
            # 1. Obtenha a instância do Cliente a partir do objeto User
            # O nome do campo no seu models.py que liga ao User
            # é o que você precisa usar aqui (o seu é 'user')
            cliente_instance = Cliente.objects.get(user=user)
            
            # 2. Use a instância do Cliente para filtrar os animais
            # O nome do campo no seu models.py que liga ao Cliente
            # é o que você precisa usar aqui (o seu é 'id_cliente')
            animais = Animal.objects.filter(id_cliente=cliente_instance)
            
            # Serializar os dados dos animais
            animais_data = AnimalSerializer(animais, many=True).data
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'email': user.email,
                'animais': animais_data
            }, status=status.HTTP_200_OK)

        except Cliente.DoesNotExist:
            return Response(
                {'error': 'Instância de Cliente não encontrada para este usuário.'},
                status=status.HTTP_400_BAD_REQUEST
            )
# ViewSet para Agendamentos (protegida com autenticação)
class AgendamentoViewSet(viewsets.ModelViewSet):
    queryset = Agendamento.objects.all().order_by('-data_agendamento', '-hora_agendamento')
    # Troque a classe do serializer para a que criamos
    serializer_class = AgendamentoSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        ## Filtra os agendamentos para retornar apenas os do cliente autenticado
        #queryset = Agendamento.objects.all().order_by('-data_agendamento', '-hora_agendamento')
        user = self.request.user
        if  not user.is_authenticated:
            return Agendamento.objects.none()  # Retorna um queryset vazio se o usuário não estiver autenticado
        
        try:
            cliente = Cliente.objects.get(user=user)
            return Agendamento.objects.filter(id_animal__id_cliente=cliente).order_by('-data_agendamento', '-hora_agendamento')
        except Cliente.DoesNotExist:
            return Agendamento.objects.none()  # Retorna um queryset vazio se o cliente não for encontrado
        
# ViewSet para listar Animais (para o dropdown do Flutter)
class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().order_by('nome')
    serializer_class = AnimalSerializer
    permission_classes = [IsAuthenticated]

# ViewSet para listar Servicos (para o dropdown do Flutter)
class ServicosViewSet(viewsets.ModelViewSet):
    queryset = Servicos.objects.all().order_by('nome_servico')
    serializer_class = ServicosSerializer
    permission_classes = [IsAuthenticated]

class AgendamentosDoDia(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Obtém a data de hoje
        hoje = datetime.now().date()
        
        # Filtra os agendamentos pela data de hoje e ordena por hora
        agendamentos = Agendamento.objects.filter(data_agendamento=hoje).order_by('hora_agendamento')

        # Serializa os dados
        serializer = AgendamentoSerializer(agendamentos, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

def agendamentos_do_dia(request):
    hoje = datetime.now().date()
    
    # Adicionamos select_related para carregar Animal e Cliente na mesma consulta
    agendamentos = Agendamento.objects.filter(data_agendamento=hoje).select_related(
        'id_animal', # Carrega o objeto Animal
        'id_animal__id_cliente' # Carrega o objeto Cliente (através do Animal)
    ).order_by('hora_agendamento')
    
    # Obtém o token do usuário logado (esta lógica está correta para o contexto do token)
    token = None
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
    
    context = {
        'hoje': hoje,
        'agendamentos': agendamentos,
        'token': token.key if token else None,
    }
    return render(request, 'agendamentos_do_dia.html', context)

# A nova view para a tela com o calendário
def listar_agendamentos(request):
    data_inicio_str = request.GET.get('data_inicio')
    data_fim_str = request.GET.get('data_fim')
    filtro_detalhes = request.GET.get('detalhes')
    
    try:
        if data_inicio_str and data_fim_str:
            data_inicio = datetime.strptime(data_inicio_str, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim_str, '%Y-%m-%d').date()
        else:
            data_inicio = date.today() - timedelta(days=7)
            data_fim = date.today() + timedelta(days=7)
    except ValueError:
        data_inicio = date.today() - timedelta(days=7)
        data_fim = date.today() + timedelta(days=7)

    # CORREÇÃO: Inicializa a queryset base, que sempre será usada.
    agendamentos_qs = Agendamento.objects.filter(
        data_agendamento__gte=data_inicio,
        data_agendamento__lte=data_fim
    ).select_related('id_servicos', 'id_animal').order_by('data_agendamento', 'hora_agendamento')

    # APLICA A FILTRAGEM ADICIONAL SE HOUVER UM TERMO DE BUSCA.
    if filtro_detalhes:
        agendamentos_qs = agendamentos_qs.filter(
            Q(id_animal__nome__icontains=filtro_detalhes) |
            Q(id_servicos__nome_servico__icontains=filtro_detalhes) |
            Q(observacoes__icontains=filtro_detalhes)
        )

    # Converte para lista somente APÓS todas as filtragens, para uso no loop.
    agendamentos = list(agendamentos_qs)

    # 2. Gera a lista de agendamentos e horários livres, agora com base na lista 'agendamentos'
    agendamentos_por_dia = {}
    delta_dias = data_fim - data_inicio
    SLOT_MINUTOS = 60 
    horario_limite = time(18, 0)
    
    for i in range(delta_dias.days + 1):
        dia_atual = data_inicio + timedelta(days=i)
        horarios_do_dia = []
        agendamentos_do_dia = [a for a in agendamentos if a.data_agendamento == dia_atual]

        # Mapeia os horários ocupados com base na duração do serviço.
        horarios_ocupados = {}
        for agendamento_atual in agendamentos_do_dia:
            duracao = agendamento_atual.id_servicos.duracao_minutos
            inicio_dt = datetime.combine(dia_atual, agendamento_atual.hora_agendamento)
            fim_dt = inicio_dt + timedelta(minutes=duracao)
            
            current_slot_dt = inicio_dt
            while current_slot_dt < fim_dt:
                horarios_ocupados[current_slot_dt.time()] = agendamento_atual
                current_slot_dt += timedelta(minutes=SLOT_MINUTOS)

        horario_slot = time(8, 0)
        
        while horario_slot < horario_limite:
            if horario_slot in horarios_ocupados:
                agendamento_no_slot = horarios_ocupados[horario_slot]
                horarios_do_dia.append({
                    'tipo': 'agendado',
                    'objeto': agendamento_no_slot
                })
            else:
                horarios_do_dia.append({
                    'tipo': 'livre',
                    'hora': horario_slot
                })
            
            horario_slot_dt = datetime.combine(dia_atual, horario_slot) + timedelta(minutes=SLOT_MINUTOS)
            horario_slot = horario_slot_dt.time()

        agendamentos_por_dia[dia_atual] = horarios_do_dia
    
    context = {
        'agendamentos_por_dia': agendamentos_por_dia,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'filtro_detalhes': filtro_detalhes,
    }
    return render(request, 'listar_agendamentos.html', context)

def agendar_servico_rapido(request):
    # --- Lógica de data_selecionada permanece a mesma ---
    data_str = request.GET.get('data')
    try:
        if data_str:
            data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
        else:
            data_selecionada = date.today()
    except ValueError:
        data_selecionada = date.today()

    agendamentos = Agendamento.objects.filter(
        data_agendamento=data_selecionada
    ).select_related('id_servicos').order_by('hora_agendamento')

    # Prepara um mapa de horários ocupados
    horarios_ocupados = {}

    # Marca todos os slots ocupados (início + duração)
    for agendamento_atual in agendamentos:
        duracao = agendamento_atual.id_servicos.duracao_minutos
        inicio_dt = datetime.combine(data_selecionada, agendamento_atual.hora_agendamento)
        fim_dt = inicio_dt + timedelta(minutes=duracao)

        current_slot_dt = inicio_dt
        while current_slot_dt < fim_dt:
            horarios_ocupados[current_slot_dt.time()] = agendamento_atual
            current_slot_dt += timedelta(minutes=60)

    # 2️⃣ Gera a lista de agendamentos e horários livres
    horarios_do_dia = []
    SLOT_MINUTOS = 60

    horario_slot = time(8, 0)
    horario_limite = time(18, 0)

    while horario_slot < horario_limite:
        if horario_slot in horarios_ocupados:
            agendamento_no_slot = horarios_ocupados[horario_slot]
            horarios_do_dia.append({
                'tipo': 'agendado',
                'objeto': agendamento_no_slot
            })
        else:
            horarios_do_dia.append({
                'tipo': 'livre',
                'hora': horario_slot
            })

        horario_slot_dt = datetime.combine(data_selecionada, horario_slot) + timedelta(minutes=SLOT_MINUTOS)
        horario_slot = horario_slot_dt.time()

    # ==========================================================
    # ✅ NOVO BLOCO — Remove horários passados no dia atual
    # ==========================================================
    if data_selecionada == datetime.now().date():
        hora_agora = datetime.now().time()
        horarios_do_dia = [
            h for h in horarios_do_dia
            if not (h['tipo'] == 'livre' and h['hora'] <= hora_agora)
        ]
        print(f"⏰ Filtrando horários do dia atual, agora {hora_agora}")

    context = {
        'horarios_do_dia': horarios_do_dia,
        'data_selecionada': data_selecionada,
    }
    return render(request, 'agendar_servico.html', context)


@login_required
def editar_agendamento(request, id):
    # Busca o agendamento pelo ID, ou retorna um erro 404 se não for encontrado
    agendamento = get_object_or_404(Agendamento, pk=id)
    titulo = "Editar Agendamento"
    
    # Lógica para salvar a edição (POST)
    if request.method == 'POST':
        form = AgendamentoForm(request.POST, instance=agendamento)
        if form.is_valid():
            form.save()
            messages.success(request, 'Agendamento atualizado com sucesso!')
            return redirect('listar_agendamentos')
        else:
            messages.error(request, 'Erro ao atualizar o agendamento. Por favor, verifique os campos.')
            
    # Lógica para exibir o formulário pré-preenchido (GET)
    else:
        # Passa a instância do agendamento para o formulário
        form = AgendamentoForm(instance=agendamento)
    
    return render(request, 'editar_agendamento.html', {'form': form, 'titulo': titulo, 'agendamento': agendamento})


@login_required
def excluir_agendamento(request, id):
    # Encontra o agendamento pelo ID, ou retorna 404
    agendamento = get_object_or_404(Agendamento, pk=id)

    # Ação de exclusão.
    agendamento.delete()
    messages.success(request, f'O agendamento para {agendamento.id_animal.nome} foi excluído com sucesso.')
    
    # Após a exclusão, redireciona para a tela de listagem
    return redirect('listar_agendamentos')


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_horarios_disponiveis(request):
    try:
        data_param = request.query_params.get('data')
        servico_id = request.query_params.get('servico_id')
        
        if not data_param or not servico_id:
            return Response(
                {"error": "Os parâmetros 'data' e 'servico_id' são obrigatórios."},
                status=400
            )

        data_selecionada = datetime.strptime(data_param, '%Y-%m-%d').date()
        servico = Servicos.objects.get(pk=servico_id)

        horarios_disponiveis = []
        hora_inicial_atendimento = time(9, 0)
        hora_final_atendimento = time(18, 0)

        # Buscar todos os agendamentos existentes para a data selecionada
        agendamentos_do_dia = Agendamento.objects.filter(data_agendamento=data_selecionada).order_by('hora_agendamento')

        # Criar uma lista de horários ocupados
        horarios_ocupados = []
        for agendamento in agendamentos_do_dia:
            inicio_ocupado = datetime.combine(data_selecionada, agendamento.hora_agendamento)
            duracao_ocupado = agendamento.id_servicos.duracao_minutos
            
            temp_hora = inicio_ocupado
            while temp_hora < inicio_ocupado + timedelta(minutes=duracao_ocupado):
                horarios_ocupados.append(temp_hora.strftime('%H:%M'))
                temp_hora += timedelta(minutes=15)

        # Gerar horários para o dia e verificar a disponibilidade
        horario_atual = datetime.combine(data_selecionada, hora_inicial_atendimento)
        while horario_atual.time() < hora_final_atendimento:
            formato_hora = horario_atual.strftime('%H:%M')
            
            # Checar se o slot de 60 minutos está livre
            is_disponivel = True
            for i in range(4):  # Verifica 4 blocos de 15 minutos
                slot_a_checar = (horario_atual + timedelta(minutes=15 * i)).strftime('%H:%M')
                if slot_a_checar in horarios_ocupados:
                    is_disponivel = False
                    break
            
            if is_disponivel:
                horarios_disponiveis.append(formato_hora)
            
            horario_atual += timedelta(minutes=60)

        # ==========================================================
        # ✅ NOVO BLOCO INSERIDO — filtra horários passados do dia atual
        # ==========================================================
        if data_selecionada == datetime.now().date():
            hora_agora = datetime.now().time()
            horarios_disponiveis = [
                h for h in horarios_disponiveis
                if datetime.strptime(h, "%H:%M").time() > hora_agora
            ]
            print(f"⏰ Filtrando horários: agora {hora_agora}, válidos: {horarios_disponiveis}")

        return Response(horarios_disponiveis, status=200)

    except Servicos.DoesNotExist:
        return Response({"error": "Serviço não encontrado."}, status=404)
    except Exception as e:
        return Response({"error": str(e)}, status=500)

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agendar_servico(request):
    try:
        id_servico = request.data.get('id_servico')
        id_animal = request.data.get('id_animal')
        data = request.data.get('data')
        hora = request.data.get('hora')

        if not all([id_servico, id_animal, data, hora]):
            return Response(
                {"detail": "Dados incompletos. 'id_servico', 'id_animal', 'data' e 'hora' são obrigatórios."},
                status=status.HTTP_400_BAD_REQUEST
            )

        servico = Servicos.objects.get(pk=id_servico)
        animal = Animal.objects.get(pk=id_animal)

        # AQUI ESTÁ A ÚNICA CORREÇÃO:
        # A view não tenta mais obter o 'cliente' do usuário.
        # A criação do agendamento não inclui o argumento 'cliente'.
        Agendamento.objects.create(
            data_agendamento=data,
            hora_agendamento=hora,
            id_animal=animal,
            id_servicos=servico
        )

        return Response(
            {"detail": "Agendamento criado com sucesso!"},
            status=status.HTTP_201_CREATED
        )

    except Servicos.DoesNotExist:
        return Response(
            {"detail": f"Serviço com ID {id_servico} não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Animal.DoesNotExist:
        return Response(
            {"detail": f"Animal com ID {id_animal} não encontrado."},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {"detail": f"Ocorreu um erro interno do servidor: {str(e)}"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ------------------------------------------------------------------
# 1. VIEW PARA SALVAR O TOKEN FCM
# ------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_fcm_token_view(request):
    """
    Recebe o token FCM do cliente logado e o salva no modelo Cliente.
    """
    token = request.data.get('fcm_token')
    user = request.user 
    
    if not token:
        return Response(
            {'error': 'FCM token não fornecido.'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Busca o Cliente usando a relação OneToOneField com o User logado
        cliente = Cliente.objects.get(user=user)
        
        cliente.fcm_token = token
        cliente.save()
        
        print(f"Token FCM salvo/atualizado para o usuário {user.username}: {token[:15]}...")
        
        return Response({'status': 'Token FCM salvo com sucesso.'}, status=status.HTTP_200_OK)
        
    except Cliente.DoesNotExist:
        print(f"ERRO: Cliente não encontrado para o usuário {user.username}. Token FCM não salvo.")
        # Se o usuário está autenticado, mas não tem um perfil de Cliente associado
        return Response(
            {'error': 'Cliente não encontrado para o usuário logado.'}, 
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        # Captura erros gerais
        print(f"ERRO ao salvar token FCM: {str(e)}")
        return Response(
            {'error': f'Erro interno ao salvar token: {str(e)}'}, 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

# ------------------------------------------------------------------
# 2. VIEW PARA FINALIZAR SERVIÇO (Dispara FCM)
# ------------------------------------------------------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def finalizar_servico(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    # 1. Atualiza o status do agendamento no banco de dados
    agendamento.status = 'finalizado'
    agendamento.save()

    try:
        # Pega o cliente do agendamento (Assumindo Agendamento -> Animal -> Cliente)
        # ATENÇÃO: Ajuste o campo 'id_cliente' se a sua relação for diferente.
        # Exemplo: cliente = agendamento.id_animal.dono_do_pet 
        cliente = agendamento.id_animal.id_cliente
        
        title = "Serviço Finalizado! 🎉"
        body = f"O serviço de {agendamento.id_servicos.nome_servico} para o seu pet {agendamento.id_animal.nome} foi finalizado. Estamos esperando você! 😊"
        
        # 2. CHAMA A FUNÇÃO DE NOTIFICAÇÃO PUSH
        send_push_notification(
            fcm_token=cliente.fcm_token, 
            title=title, 
            body=body
        )
        
    except Cliente.DoesNotExist:
        print(f"AVISO: Cliente associado ao agendamento {pk} não encontrado. Notificação falhou.")
    except Exception as e:
        print(f"ERRO ao tentar enviar notificação para agendamento {pk}: {e}")

    # Retorna o agendamento atualizado.
    # Presumo que você tenha um AgendamentoSerializer importado e funcional.
    # serializer = AgendamentoSerializer(agendamento)
    # return Response(serializer.data)
    
    # Retorno simples sem serializer, caso não esteja definido
    return Response({'status': 'Serviço finalizado com sucesso. Notificação push tentada.'}, status=status.HTTP_200_OK)
