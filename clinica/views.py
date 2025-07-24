from django.shortcuts import render, redirect,  get_object_or_404
from .models import Cliente, Animal, Veterinario
from .forms import ClienteForm, AnimalForm, VeterinarioForm, VacinaForm
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

    consultas = animal.consulta_set.select_related('id_veterinario').all()
    vacinas = animal.aplicacaovacina_set.select_related('id_veterinario', 'id_vacina').all()
    tratamentos = animal.realizacaotratamento_set.select_related('id_veterinario', 'id_tratamento').all()

    historico = []

    for c in consultas:
        historico.append({
            'data': c.data_consulta,
            'tipo': 'Consulta',
            'descricao': c.descricao,
            'veterinario': c.id_veterinario.nome,
        })

    for v in vacinas:
        historico.append({
            'data': v.data_aplicacao,
            'tipo': 'Vacina - ' + v.id_vacina.nome_vacina,
            'descricao': f"Tipo: {v.id_vacina.tipo_vacina}",
            'veterinario': v.id_veterinario.nome,
        })

    for t in tratamentos:
        historico.append({
            'data': t.data_realizacao,
            'tipo': 'Tratamento - ' + t.id_tratamento.nome_tratamento,
            'descricao': t.observacoes,
            'veterinario': t.id_veterinario.nome,
        })

    # Ordena todos os registros pela data decrescente
    historico.sort(key=lambda x: x['data'], reverse=True)

    return render(request, 'historico_clinico.html', {
        'animal': animal,
        'historico': historico
    })


