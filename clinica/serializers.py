# clinica/serializers.py

from rest_framework import serializers
from .models import Agendamento, Animal, Servicos

# Serializer para o modelo Animal (necessário para listar os nomes)
class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = ['id', 'nome']

# Serializer para o modelo Servicos (para o dropdown no Flutter)
class ServicosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servicos
        fields = ['id', 'nome_servico']

# Serializer principal para o agendamento

class AgendamentoSerializer(serializers.ModelSerializer):
    # Campos de leitura
    nome_cliente = serializers.SerializerMethodField()
    nome_animal = serializers.SerializerMethodField()
    nome_servico = serializers.SerializerMethodField()

    class Meta:
        model = Agendamento
        fields = [
            'id',
            'id_animal',
            'id_servicos',
            'data_agendamento',
            'hora_agendamento',
            'observacoes',
            'nome_cliente',
            'nome_animal',
            'nome_servico',
        ]
        read_only_fields = [
            'nome_cliente', 
            'nome_animal', 
            'nome_servico'
        ]

    def get_nome_cliente(self, obj):
        # Percorre a relação: Agendamento -> Animal -> Cliente -> nome_completo
        return obj.id_animal.id_cliente.nome_completo if obj.id_animal and obj.id_animal.id_cliente else None

    def get_nome_animal(self, obj):
        return obj.id_animal.nome if obj.id_animal else None

    def get_nome_servico(self, obj):
        return obj.id_servicos.nome_servico if obj.id_servicos else None
