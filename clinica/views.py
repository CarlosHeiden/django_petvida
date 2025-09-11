from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect,  get_object_or_404
from django.db.models import Q 
from django.http import JsonResponse
from .models import Cliente, Veterinario, Animal, Vacina, Consulta,Tratamento, AplicacaoVacina, RealizacaoTratamento, Veterinario, Agendamento, Servicos
from .forms import CadastroForm, ClienteForm, AnimalForm, VeterinarioForm, VacinaForm,  AplicacaoVacinaForm, AgendamentoForm, ConsultaForm, RealizacaoTratamentoForm
from datetime import datetime, timedelta, time, date

from .serializers import AgendamentoSerializer, AnimalSerializer, ServicosSerializer
from rest_framework.decorators import api_view
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView





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

@login_required
def cadastrar_agendamento(request):
    DURACAO_SERVICOS = {
        'Banho': 60,
        'Tosa': 60,
        'Banho e Tosa': 120,
    }
    servicos_sem_vet = list(DURACAO_SERVICOS.keys())

    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            servicos = form.cleaned_data['id_servicos']
            data = form.cleaned_data['data_agendamento']
            hora = form.cleaned_data['hora_agendamento']
            

            conflito_encontrado = False

            if tipo_servico in servicos_sem_vet:
                # DEBUG: Imprime o tipo de serviço e data que estamos processando
                print(f"\n--- DEPURAÇÃO DE AGENDAMENTO SEM VET ---")
                print(f"Tentando agendar '{tipo_servico}' para a data: {data}")

                agendamentos_existentes = Agendamento.objects.filter(
                    data_agendamento=data,
                    tipo_servico__in=servicos_sem_vet
                ).order_by('hora_agendamento') # Ordena para facilitar a leitura
                
                # DEBUG: Mostra a lista de agendamentos existentes encontrados
                print(f"Agendamentos existentes encontrados: {agendamentos_existentes.count()}")
                for agendamento in agendamentos_existentes:
                    print(f"-> Horário existente: {agendamento.hora_agendamento}, Tipo: {agendamento.tipo_servico}")

                duracao = DURACAO_SERVICOS.get(tipo_servico, 60)
                horario_inicio_novo = datetime.combine(data, hora)
                horario_fim_novo = horario_inicio_novo + timedelta(minutes=duracao)

                conflitos_encontrados = []
                for agendamento_existente in agendamentos_existentes:
                    horario_inicio_existente = datetime.combine(agendamento_existente.data_agendamento, agendamento_existente.hora_agendamento)
                    duracao_existente = DURACAO_SERVICOS.get(agendamento_existente.tipo_servico, 60)
                    horario_fim_existente = horario_inicio_existente + timedelta(minutes=duracao_existente)
                    
                    # Verifica a sobreposição
                    if not (horario_fim_novo <= horario_inicio_existente or horario_inicio_novo >= horario_fim_existente):
                        conflitos_encontrados.append(agendamento_existente)
                
                if conflitos_encontrados:
                    # DEBUG: Encontrou conflito. Mostra a lógica para encontrar o próximo horário.
                    print("Conflito encontrado. Buscando próximo horário disponível...")
                    proximo_horario = encontrar_proximo_horario_disponivel(data, duracao, agendamentos_existentes)
                    
                    if proximo_horario:
                        mensagem_erro = f'Já existe um agendamento que se sobrepõe a este horário. O próximo horário disponível é às **{proximo_horario.strftime("%H:%M")}**.'
                    else:
                        mensagem_erro = 'Não há horários disponíveis para este serviço neste dia.'
                    
                    messages.error(request, mensagem_erro)
                    conflito_encontrado = True
                else:
                    form.instance.id_veterinario = None
            else:
                # Lógica para agendamentos com veterinário permanece a mesma
                agendamentos_conflitantes = Agendamento.objects.filter(
                    data_agendamento=data,
                    hora_agendamento=hora,
                    id_veterinario=veterinario
                )
                
                if agendamentos_conflitantes.exists():
                    messages.error(request, 'Este horário já está agendado para o veterinário selecionado.')
                    conflito_encontrado = True

            if not conflito_encontrado:
                form.save()
                messages.success(request, 'Serviço agendado com sucesso!')
                return redirect('cadastrar_agendamento')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"Erro no campo '{field}': {error}")
            
    else:
        form = AgendamentoForm()
    
    return render(request, 'formulario.html', {
        'form': form,
        'titulo': 'Agendar Serviços'
    })


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
   # queryset = Agendamento.objects.all().order_by('-data_agendamento', '-hora_agendamento')
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
    agendamentos = Agendamento.objects.filter(data_agendamento=hoje).order_by('hora_agendamento')
    
    # Obtém o token do usuário logado
    token = None
    if request.user.is_authenticated:
        token, created = Token.objects.get_or_create(user=request.user)
    
    context = {
        'hoje': hoje,
        'agendamentos': agendamentos,
        'token': token.key if token else None, # Adiciona a chave do token ao contexto
    }
    return render(request, 'agendamentos_do_dia.html', context)


def get_agendamentos_json(request):
    """
    Retorna os agendamentos do dia em formato JSON para o JavaScript.
    Não exige autenticação de token.
    """
    hoje = date.today()
    agendamentos = Agendamento.objects.filter(data_agendamento=hoje).order_by('hora_agendamento')
    serializer = AgendamentoSerializer(agendamentos, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def finalizar_servico(request, pk):
    agendamento = get_object_or_404(Agendamento, pk=pk)
    
    # Atualiza o status do agendamento no banco de dados
    agendamento.status = 'finalizado'
    agendamento.save()

    # Lógica para enviar a mensagem (exemplo simples)
    # Você pode integrar com uma API de SMS ou WhatsApp aqui
    mensagem_cliente = f"Olá, {agendamento.id_animal.id_cliente.nome_completo}! O serviço de {agendamento.id_servicos.nome_servico} para o seu pet {agendamento.id_animal.nome} foi finalizado. 😊"
    print("MENSAGEM PARA O CLIENTE:", mensagem_cliente) # Exemplo: apenas imprime no console

    serializer = AgendamentoSerializer(agendamento)
    return Response(serializer.data)




