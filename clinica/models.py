from django.db import models
from django.contrib.auth.models import User

# Adicione o OneToOneField para ligar o Cliente ao User do Django
class Cliente(models.Model):
    # RELAÇÃO OBRIGATÓRIA: Liga o Cliente ao User nativo do Django
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuário")
    
    nome_completo = models.CharField("Nome completo", max_length=100)
    cpf = models.CharField("CPF", max_length=14, unique=True)
    telefone = models.CharField("Telefone", max_length=20)
    email = models.EmailField("Email", blank=True, null=True)
    endereco = models.CharField("Endereço", max_length=255)

    # NOVO CAMPO: Para armazenar o token do Firebase Cloud Messaging
    fcm_token = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name='Token FCM do Dispositivo'
    )

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"

class Animal(models.Model):
    nome = models.CharField("Nome do animal", max_length=100)
    especie = models.CharField("Espécie", max_length=50)
    raca = models.CharField("Raça", max_length=50)
    data_nascimento = models.DateField("Data de nascimento")
    porte = models.CharField("Porte", max_length=30)
    peso = models.DecimalField("Peso (kg)", max_digits=5, decimal_places=2)
    id_cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Tutor")

    def __str__(self):
        return f"{self.nome} - {self.especie} ({self.id_cliente.nome_completo})"

class Veterinario(models.Model):
    nome = models.CharField("Nome", max_length=100)
    crmv = models.CharField("CRMV", max_length=20, unique=True)
    especialidade = models.CharField("Especialidade", max_length=100)
    telefone = models.CharField("Telefone", max_length=20)

    def __str__(self):
        return f"{self.nome} ({self.especialidade})"

class Consulta(models.Model):
    id_animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    id_veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, verbose_name="Veterinário")
    data_consulta = models.DateField("Data da consulta")
    hora_consulta = models.TimeField("Hora da consulta")
    descricao = models.TextField("Descrição do atendimento")

    def __str__(self):
        return f"Consulta de {self.id_animal.nome} em {self.data_consulta}"

class Vacina(models.Model):
    nome_vacina = models.CharField("Nome da vacina", max_length=100)
    tipo_vacina = models.CharField("Tipo", max_length=50)

    def __str__(self):
        return f"{self.nome_vacina} ({self.tipo_vacina})"

class AplicacaoVacina(models.Model):
    id_animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    id_vacina = models.ForeignKey(Vacina, on_delete=models.CASCADE, verbose_name="Vacina")
    id_veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, verbose_name="Veterinário")
    data_aplicacao = models.DateField("Data de aplicação")

    def __str__(self):
        return f"{self.id_vacina.nome_vacina} - {self.id_animal.nome} em {self.data_aplicacao}"

class Tratamento(models.Model):
    nome_tratamento = models.CharField("Nome do tratamento", max_length=100)
    tipo_tratamento = models.CharField("Tipo de Tratamento", max_length=50 , default="teste")
    descricao = models.TextField("Descrição")

    def __str__(self):
        return self.nome_tratamento

class RealizacaoTratamento(models.Model):
    id_animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    id_tratamento = models.ForeignKey(Tratamento, on_delete=models.CASCADE, verbose_name="Tratamento")
    id_veterinario = models.ForeignKey(Veterinario, on_delete=models.SET_NULL, null=True, verbose_name="Veterinário")
    data_realizacao = models.DateField("Data de realização")
    observacoes = models.TextField("Observações")

    def __str__(self):
        return f"{self.id_tratamento.nome_tratamento} - {self.id_animal.nome} em {self.data_realizacao}"

class Servicos(models.Model):
    nome_servico = models.CharField("Nome do serviço", max_length=100)
    duracao_minutos = models.IntegerField("Duração em minutos", default=60) # NOVO CAMPO
    
    def __str__(self):
        return self.nome_servico

class Agendamento(models.Model):
    id_animal = models.ForeignKey(Animal, on_delete=models.CASCADE, verbose_name="Animal")
    id_servicos = models.ForeignKey(Servicos, on_delete=models.SET_NULL, null=True, verbose_name="Serviço")
    data_agendamento = models.DateField("Data")
    hora_agendamento = models.TimeField("Hora")
    observacoes = models.TextField("Observações", blank=True, null=True)
    status = models.CharField(max_length=20, default='pendente') # Novo campo de status

    # Corrigido o __str__ para usar o nome do serviço
    def __str__(self):
        # Proteção contra id_servicos ser nulo
        servico_nome = self.id_servicos.nome_servico if self.id_servicos else "Serviço não especificado"
        return f"{servico_nome} - {self.id_animal.nome} em {self.data_agendamento}"