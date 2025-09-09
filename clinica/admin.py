from django.contrib import admin

from django.contrib import admin
from .models import (
    Cliente, Animal, Veterinario, Consulta,
    Vacina, AplicacaoVacina, Tratamento,
    RealizacaoTratamento, Agendamento, Servicos
)

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
