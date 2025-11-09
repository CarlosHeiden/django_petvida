from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .models import Cliente, Animal, Servicos, Agendamento, Vacina, AplicacaoVacina, Tratamento, RealizacaoTratamento, Veterinario, Consulta

admin.site.register(Cliente)
admin.site.register(Animal)
admin.site.register(Veterinario)
admin.site.register(Consulta)
admin.site.register(Vacina)
admin.site.register(AplicacaoVacina)
admin.site.register(Tratamento)
admin.site.register(RealizacaoTratamento)
admin.site.register(Agendamento)
admin.site.register(Servicos)
