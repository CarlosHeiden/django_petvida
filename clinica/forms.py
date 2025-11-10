from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import HiddenInput
from .models import (
    Cliente, Animal, Veterinario, Vacina,
    Consulta, AplicacaoVacina, Tratamento,
    RealizacaoTratamento, Agendamento
)
from datetime import datetime, timedelta




class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'nome_completo': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
        }

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'crmv': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidade': forms.TextInput(attrs={'class': 'form-control'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control'}),
        }

class AnimalForm(forms.ModelForm):
    ESPECIES_CHOICES = [
        ('', 'Selecione a especie do animal'),  # valor vazio para ser o placeholder
        ('Cachorro', 'Cachorro'),
        ('Gato', 'Gato'),
    ]

    PORTE_CHOICES = [
        ('', 'Selecione o porte'),  # placeholder
        ('Pequeno', 'Pequeno'),
        ('Médio', 'Médio'),
        ('Grande', 'Grande'),
    ]

    especie = forms.ChoiceField(
        choices=ESPECIES_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Espécie"
    )

    porte = forms.ChoiceField(
        choices=PORTE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Porte"
    )

    class Meta:
        model = Animal
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_cliente': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Selecione o tutor'
            }),
        }

    # 🔧 Ajuste para o dropdown do tutor (cliente)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_cliente'].empty_label = "Selecione o tutor"



class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = '__all__'
        widgets = {
            'nome_vacina': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_vacina': forms.TextInput(attrs={'class': 'form-control'}),
        }

class ConsultaForm(forms.ModelForm):
    class Meta:
        model = Consulta
        fields = '__all__'
        widgets = {
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_veterinario': forms.Select(attrs={'class': 'form-control'}),
            'data_consulta': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_consulta': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

class AplicacaoVacinaForm(forms.ModelForm):
    class Meta:
        model = AplicacaoVacina
        fields = '__all__'
        widgets = {
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_vacina': forms.Select(attrs={'class': 'form-control'}),
            'id_veterinario': forms.Select(attrs={'class': 'form-control'}),
            'data_aplicacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class TratamentoForm(forms.ModelForm):
    class Meta:
        model = Tratamento
        fields = '__all__'
        widgets = {
            'nome_tratamento': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_tratamento': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control'}),
        }

class RealizacaoTratamentoForm(forms.ModelForm):
    class Meta:
        model = RealizacaoTratamento
        fields = '__all__'
        widgets = {
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_tratamento': forms.Select(attrs={'class': 'form-control'}),
            'id_veterinario': forms.Select(attrs={'class': 'form-control'}),
            'data_realizacao': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }

# Defina suas opções de serviço aqui
OPCOES_SERVICO = [
    ('Tosa', 'Tosa'),
    ('Banho', 'Banho'),
    ('Banho e Tosa', 'Banho e Tosa'),
]

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = ['id_animal', 'id_servicos', 'data_agendamento', 'hora_agendamento', 'observacoes']
        widgets = {
            # CAMPOS VISÍVEIS: Têm que ter a classe de estilo aqui!
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_servicos': forms.Select(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),

            # CAMPOS OCULTOS: Não precisam de classe de estilo
            'data_agendamento': HiddenInput(), 
            'hora_agendamento': HiddenInput(),
        }

     # --- MODIFICAÇÃO CRÍTICA NO MÉTODO clean() ---
    def clean(self):
        cleaned_data = super().clean()
        data_agendamento = cleaned_data.get('data_agendamento')
        hora_agendamento = cleaned_data.get('hora_agendamento')
        servico = cleaned_data.get('id_servicos')

        # Se os dados estiverem ausentes, o erro já será retornado por outros validadores
        if not data_agendamento or not hora_agendamento or not servico:
            return cleaned_data

        duracao = servico.duracao_minutos
        
        # Constrói o intervalo de tempo do novo agendamento
        data_hora_inicio = datetime.combine(data_agendamento, hora_agendamento)
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao)

        # Busca por agendamentos que se sobrepõem, MAS...
        # ...EXCLUI O AGENDAMENTO ATUAL da busca se ele estiver sendo editado.
        agendamentos_existentes = Agendamento.objects.filter(
            data_agendamento=data_agendamento
        ).exclude(id=self.instance.id) # <- ESSA É A LINHA QUE FAZ A DIFERENÇA

        # Verifica se há sobreposição com outros agendamentos
        for agendamento in agendamentos_existentes:
            duracao_existente = agendamento.id_servicos.duracao_minutos
            inicio_existente = datetime.combine(agendamento.data_agendamento, agendamento.hora_agendamento)
            fim_existente = inicio_existente + timedelta(minutes=duracao_existente)
            
            # Checa se o novo agendamento se sobrepõe ao existente
            if max(data_hora_inicio, inicio_existente) < min(data_hora_fim, fim_existente):
                raise forms.ValidationError(
                    "Este horário se sobrepõe a um agendamento existente. Por favor, escolha outro horário."
                )
        
        return cleaned_data



# Crie um novo formulário de registro
class CadastroForm(UserCreationForm):
    # Campos que você quer adicionar no formulário de registro
    # O UserCreationForm já tem 'username' e 'password'
    
    # Adicionando um campo de email
    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = User
        fields = ('username', 'email') # Apenas os campos que queremos mostrar
        labels = {
            'username': 'Nome de Usuário',
            'password': 'Senha',
            'email': 'Email',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }