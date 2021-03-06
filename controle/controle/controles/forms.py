from django import forms

from .models import Categoria, Subcategoria, NotaFiscal, Manual, Item, Equipamento, Emprestimo, Devolucao

class CategoriaForm(forms.ModelForm):
	class Meta:
		model = Categoria
		fields = ['nome','abreviacao']
		widgets ={
			'nome':forms.TextInput(attrs={'autofocus': 'autofocus'})
		}

class SubcategoriaForm(forms.ModelForm):
	class Meta:
		model = Subcategoria
		fields = ['nome']

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

def getListEquipamento():
	equipamentos = Equipamento.objects.all()
	equipamento_list = []
	for equipamento in equipamentos:
		equipamento_list.append(equipamento.id_item.id_item)
	return equipamento_list

class EquipamentoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
    	eq = Equipamento.objects.get(id_item=obj.id_item)
    	return eq.patrimonio_itti + ' ' + obj.nome

class ItemForm(forms.ModelForm):
	#Dinamico - atualiza modelchoicefield
	def __init__(self, *args, **kwargs):
		super(ItemForm, self).__init__(*args, **kwargs)
		self.fields['id_equipamento_pertencente'].queryset = Item.objects.filter(id_item__in=getListEquipamento())

	class Meta:
		model = Item
		fields = [
					'nome',
					'marca','modelo',
					'categoria',
					'subcategoria',
					'caracteristica',
					'id_equipamento_pertencente',
					'projeto',
					'ano',
					'id_departamento', 
					'local', 
					'id_notafiscal',
					'valor',
					'tipo_consumivel',
					 'quantidade', 
					 'validade'
					 
				]
		#fields = '__all__'		
		widgets = {
            'validade': DateInput(),
         }
	id_equipamento_pertencente = EquipamentoModelChoiceField(required=False, widget=forms.Select, queryset = Item.objects.none())

# class ItemForm(forms.Form):
# 	name           = forms.CharField(label='Nome', widget=forms.TextInput(attrs={"placeholder":"Fantasia"}))
# 	marca		   = forms.CharField(label='Marca', initial='Genérico', widget=forms.TextInput(attrs={"placeholder":"Codigo"}))
# 	modelo 		   = forms.CharField(label='Modelo', widget=forms.TextInput(attrs={"placeholder":"Codigo"}))
# 	categoria 	   = forms.ModelChoiceField(queryset = Categoria.objects.all())
#	subcategoria   = forms.ModelChoiceField(queryset = Subcategoria.objects.all())
#	id_equipamento_pertencente = forms.ModelChoiceField(queryset = Equipamentos.objects.all())
#	
# 	caracteristica = forms.CharField(
# 							label='Característica',
# 							required=False,
# 							widget=forms.Textarea(
# 								attrs={
# 										"class": "input-class",
# 										"id":"my-id-for-area",
# 										"rows":5,
# 										'cols':30
# 									}

# 								)
# 							)
#	projeto = forms.

class EquipamentoForm(forms.ModelForm):
	class Meta:
		model = Equipamento
		fields = ['patrimonio_itti','patrimonio_ufpr','id_manual']



class ItemEquipamentoForm(forms.ModelForm):
	class Meta:
		model = Item
		fields = [
					'nome',
					'marca','modelo',
					'categoria',
					'subcategoria',
					'caracteristica',
					'projeto',
					'ano',
					'id_departamento', 
					'local', 
					'id_notafiscal',
					'valor'
					 
				]


def getListItensDisponiveis():
	itens = Item.objects.all()
	item_list = []
	for item in itens:
		if item.status_emprestado is False:
			item_list.append(item.id_item)
	return item_list

class ItemModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
    	item = Item.objects.get(id_item=obj.id_item)
    	return str(item.id_item) + ' ' + item.nome


class EmprestimoForm(forms.ModelForm):
	#Dinamico - atualiza modelchoicefield
	def __init__(self, *args, **kwargs):
		super(EmprestimoForm, self).__init__(*args, **kwargs)
		self.fields['id_item'].queryset = Item.objects.filter(id_item__in=getListItensDisponiveis())

	class Meta:
		model = Emprestimo
		fields = '__all__'

	id_item = ItemModelChoiceField(required=False, widget=forms.Select, queryset = Item.objects.none())



def getListEmprestimoPendentes():
	devolucoes = Devolucao.objects.all()
	devolucoes_list =[]
	for devolucao in devolucoes:
		devolucoes_list.append(devolucao.emprestimo.pk)
	return devolucoes_list


class EmprestimoModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
    	emprestimo = Emprestimo.objects.get(pk=obj.pk)
    	return str(emprestimo.id_item.nome) + ' ' + emprestimo.cpf.nome


class DevolucaoForm(forms.ModelForm):
	#Dinamico - atualiza modelchoicefield
	def __init__(self, *args, **kwargs):
		super(DevolucaoForm, self).__init__(*args, **kwargs)
		self.fields['emprestimo'].queryset = Emprestimo.objects.all().exclude(pk__in=getListEmprestimoPendentes())

	class Meta:
		model = Devolucao
		fields = '__all__'

	emprestimo = EmprestimoModelChoiceField(required=False, widget=forms.Select, queryset = Emprestimo.objects.none())