from django.contrib import admin

# Register your models here.
from controles.models import Departamento, Projeto

admin.site.register(Departamento)

admin.site.register(Projeto)