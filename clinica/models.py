# models.py (trecho substituto para a model Cliente + signal)
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import IntegrityError

class Cliente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome_completo = models.CharField("Nome completo", max_length=100)
    telefone = models.CharField(max_length=30, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    cpf = models.CharField(max_length=20, unique=True)
    fcm_token = models.CharField(
        max_length=255, 
        null=True, 
        blank=True, 
        verbose_name='Token FCM do Dispositivo'
    )

    def __str__(self):
        return f"{self.nome_completo} ({self.cpf})"

@receiver(post_save, sender=Cliente)
def criar_usuario_automatico(sender, instance: Cliente, created, **kwargs):
    """
    Ao criar um Cliente (created == True) e se não houver user vinculado,
    cria automaticamente um User Django vinculado ao Cliente.

    - Username: preferencialmente o email; se vazio, usa CPF.
    - Senha: usa o telefone informado (por isso é necessário ajustar os validadores).
    - Se username já existir, adiciona sufixo numérico (username, username_1, ...)
    """
    # Apenas quando o Cliente foi criado e não tem user associado
    if not created or instance.user:
        return

    # Determinar username e password
    base_username = (instance.email or instance.cpf or instance.nome_completo or "user").strip()
    # Limpeza simples (remover espaços)
    base_username = base_username.replace(" ", "_")
    if base_username == "":
        base_username = "user"

    password = (instance.telefone or "").strip()
    if password == "":
        # fallback mínimo; ideal: não permitir criar sem telefone se for usada como senha
        password = "petvida_default_pwd"

    # Garante que username seja único
    username = base_username
    suffix = 0
    while True:
        if not User.objects.filter(username=username).exists():
            break
        suffix += 1
        username = f"{base_username}_{suffix}"

    try:
        # Cria usuário — se você tiver desabilitado AUTH_PASSWORD_VALIDATORS em settings,
        # isso não será barrado. Caso contrário, pode lançar ValidationError.
        user = User.objects.create_user(username=username, email=(instance.email or ""), password=password)
        # opcional: ajustar atributos do user
        user.first_name = instance.nome_completo or ""
        user.save(update_fields=["first_name"])

        # vincula o user ao cliente e salva (update_fields evita set off many things)
        instance.user = user
        # salva apenas o campo user para evitar triggers desnecessários
        instance.save(update_fields=["user"])

        print(f"✅ Usuário criado automaticamente para Cliente(id={instance.pk}): username='{username}'")
    except IntegrityError as ie:
        print(f"❌ IntegrityError ao criar User para Cliente(id={instance.pk}): {ie}")
    except Exception as e:
        # Ex.: validação de senha, problemas inesperados
        print(f"❌ Erro ao criar User automático para Cliente(id={instance.pk}): {e}")

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