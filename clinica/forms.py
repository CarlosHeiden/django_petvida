from django import forms
from .models import Cliente, Animal, Veterinario, Vacina

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = '__all__'

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = '__all__'

class VacinaForm(forms.ModelForm):
    class Meta:
        model = Vacina
        fields = '__all__'
