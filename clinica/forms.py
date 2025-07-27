from django import forms
from .models import (
    Cliente, Animal, Veterinario, Vacina,
    Consulta, AplicacaoVacina, Tratamento,
    RealizacaoTratamento, Agendamento
)

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

class AgendamentoForm(forms.ModelForm):
    class Meta:
        model = Agendamento
        fields = '__all__'
        widgets = {
            'id_animal': forms.Select(attrs={'class': 'form-control'}),
            'id_veterinario': forms.Select(attrs={'class': 'form-control'}),
            'data_agendamento': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora_agendamento': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'tipo_servico': forms.TextInput(attrs={'class': 'form-control'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control'}),
        }
