from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
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
    class Meta:
        model = Animal
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'especie': forms.TextInput(attrs={'class': 'form-control'}),
            'raca': forms.TextInput(attrs={'class': 'form-control'}),
            'data_nascimento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'porte': forms.TextInput(attrs={'class': 'form-control'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control'}),
            'id_cliente': forms.Select(attrs={'class': 'form-control'}),
        }

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
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_servicos': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_agendamento': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        data = cleaned_data.get('data_agendamento')
        hora = cleaned_data.get('hora_agendamento')
        servico = cleaned_data.get('id_servicos')
        
        # Só valida se todos os campos necessários estão preenchidos
        if data and hora and servico:
            # Pega a duração do serviço do modelo
            duracao = servico.duracao_minutos
            
            # Converte a data e a hora para um objeto datetime
            horario_inicio_novo = datetime.combine(data, hora)
            horario_fim_novo = horario_inicio_novo + timedelta(minutes=duracao)
            
            # Filtra por agendamentos existentes na mesma data
            agendamentos_existentes = Agendamento.objects.filter(data_agendamento=data)

            # Para cada agendamento existente, verifica a sobreposição
            for agendamento_existente in agendamentos_existentes:
                duracao_existente = agendamento_existente.id_servicos.duracao_minutos
                horario_inicio_existente = datetime.combine(agendamento_existente.data_agendamento, agendamento_existente.hora_agendamento)
                horario_fim_existente = horario_inicio_existente + timedelta(minutes=duracao_existente)
                
                # Lógica de sobreposição
                if not (horario_fim_novo <= horario_inicio_existente or horario_inicio_novo >= horario_fim_existente):
                    raise forms.ValidationError('Este horário se sobrepõe a um agendamento existente. Por favor, escolha outro horário.')
        
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