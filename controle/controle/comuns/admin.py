from django.contrib import admin

# Register your models here.
from controles.models import Departamento, Projeto, Pessoa, Funcionario

admin.site.register(Departamento)

admin.site.register(Projeto)

admin.site.register(Pessoa)

admin.site.register(Funcionario)