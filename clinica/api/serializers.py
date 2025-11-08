# clinica/api/serializers.py
from datetime import datetime, timedelta
from rest_framework import serializers
from clinica.models import Agendamento, Animal, Servicos, Cliente

class AgendamentoSerializer(serializers.ModelSerializer):
    # Adicionamos campos para o nome do animal e do serviço,
    # que são usados para a visualização no Flutter.
    nome_animal = serializers.CharField(source='id_animal.nome', read_only=True)
    nome_servico = serializers.CharField(source='id_servicos.nome_servico', read_only=True)

    class Meta:
        model = Agendamento
        fields = [
            'id', 'id_animal', 'nome_animal', 'id_servicos', 'nome_servico',
            'data_agendamento', 'hora_agendamento', 'observacoes', 'status'
        ]

    # --- LÓGICA DE VALIDAÇÃO DE SOBREPOSIÇÃO (IDÊNTICA À DO FORMS.PY) ---
    def validate(self, data):
        data_agendamento = data.get('data_agendamento')
        hora_agendamento = data.get('hora_agendamento')
        servico = data.get('id_servicos')

        if not all([data_agendamento, hora_agendamento, servico]):
            # A validação de campos obrigatórios é feita automaticamente,
            # então podemos retornar aqui se algum campo estiver faltando.
            return data

        duracao = servico.duracao_minutos
        
        data_hora_inicio = datetime.combine(data_agendamento, hora_agendamento)
        data_hora_fim = data_hora_inicio + timedelta(minutes=duracao)

        # Verifica se o agendamento já existe (para edições)
        instance = self.instance
        
        agendamentos_existentes = Agendamento.objects.filter(
            data_agendamento=data_agendamento
        )

        # Exclui o agendamento atual da validação de sobreposição, se estivermos editando.
        if instance:
            agendamentos_existentes = agendamentos_existentes.exclude(pk=instance.pk)
        
        for agendamento in agendamentos_existentes:
            duracao_existente = agendamento.id_servicos.duracao_minutos
            inicio_existente = datetime.combine(agendamento.data_agendamento, agendamento.hora_agendamento)
            fim_existente = inicio_existente + timedelta(minutes=duracao_existente)
            
            if max(data_hora_inicio, inicio_existente) < min(data_hora_fim, fim_existente):
                raise serializers.ValidationError(
                    "Este horário se sobrepõe a um agendamento existente. Por favor, escolha outro horário."
                )
        
        return data
    
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

# Serializer para o modelo Cliente (se necessário no futuro)
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nome_completo', 'email', 'telefone']    