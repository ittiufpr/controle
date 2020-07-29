from django import forms

from .models import Departamento, Categoria, Subcategoria, Projeto, NotaFiscal, Manual, Item, Equipamento

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		fields = ['nome']
		labels = {'nome':''}

class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['nome']

class SubcategoriaForm(forms.ModelForm):
	class Meta:
		model = Subcategoria
		fields = ['nome']


class ProjetoForm(forms.ModelForm):
	class Meta:
		model = Projeto
		fields = ['nome','acronimo']


class NotaFiscalForm(forms.ModelForm):
	class Meta:
		model = NotaFiscal
		fields = ['nome','documento']

class ManualForm(forms.ModelForm):
	class Meta:
		model = Manual
		fields = ['nome','documento']


class DateInput(forms.DateInput):
    input_type = 'date'

class ItemForm(forms.ModelForm):
	class Meta:
		model = Item
		#fields = ['nome','caracteristica','marca','modelo','categoria','subcategoria','projeto','valor','local', 'id_departamento', 'id_notafiscal','status_disponivel','status_manutencao','status_emprestado','tipo_consumivel', 'quantidade', 'validade','id_equipamento_pertencente']
		fields = '__all__'		
		widgets = {
            'validade': DateInput()
        }

class EquipamentoForm(forms.ModelForm):
	class Meta:
		model = Equipamento
		fields = ['patrimonio_itti','patrimonio_ufpr','id_manual']

