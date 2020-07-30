from django.contrib import admin

from controles.models import Categoria, Manual, NotaFiscal, Item, Equipamento, Subcategoria


#Gerenciamento
admin.site.register(Categoria)
admin.site.register(Subcategoria)
admin.site.register(Manual)
admin.site.register(NotaFiscal)
admin.site.register(Item)
admin.site.register(Equipamento)
# Register your models here.
