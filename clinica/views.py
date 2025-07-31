from django.shortcuts import render, redirect,  get_object_or_404
from .models import Cliente, Animal, Veterinario
from .forms import ClienteForm, AnimalForm, VeterinarioForm, VacinaForm,  AplicacaoVacinaForm, AgendamentoForm, ConsultaForm, RealizacaoTratamentoForm
from .models import Cliente, Veterinario, Animal, Vacina, Consulta,Tratamento, AplicacaoVacina, RealizacaoTratamento, Veterinario
from django.db.models import Q 

def menu(request):
    return render(request, 'menu.html')

def cadastrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = ClienteForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Cliente'})

def cadastrar_animal(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = AnimalForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Animal'})

def cadastrar_veterinario(request):
    if request.method == 'POST':
        form = VeterinarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = VeterinarioForm()
    return render(request, 'formulario.html', {'form': form, 'titulo': 'Cadastrar Veterinário'})

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
def cadastrar_agendamento(request):
    if request.method == 'POST':
        form = AgendamentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = AgendamentoForm()
    return render(request, 'formulario.html', {
        'form': form,
        'titulo': 'Agendar Atendimento'
    })

# REALIZAÇÃO DE TRATAMENTO
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
