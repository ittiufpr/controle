from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#import Models
from .models import Categoria, Subcategoria, NotaFiscal, Manual, Item, Equipamento

#import Model Comuns
from comuns.models import Projeto, Departamento

from .forms import CategoriaForm, SubcategoriaForm, NotaFiscalForm, ManualForm, ItemForm, EquipamentoForm, ItemEquipamentoForm

#pdf imports
from django.template.loader import get_template, render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views import View

#Erro to delete protected
from django.db.models import ProtectedError
from django.db import IntegrityError

from django.conf import settings
import datetime
import os
import time
from django.db.models.signals import post_save

from django.http import JsonResponse

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy


from django.forms.models import inlineformset_factory


##################### GERADOR DE PDF ################################



def fetch_resources(uri, rel):
    path = os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    print(path)
    return path


def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-16")), dest=result, link_callback=fetch_resources)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None


def data_to_pdf(request):
	data1 ={
		"ano":'2000',
		"projeto": 'BR135',
		"itti":'WKST001/20'
	}

	pdf_view(request)

#pega todos os itens de um equipamento
def itens_equipamento(id_item):
	itens = Item.objects.filter(id_equipamento_pertencente=id_item).order_by('nome')
	itens_equipamento = []
	for item in itens:
		if (int(item.id_item)!=int(id_item)):
			itens_equipamento.append(item)
	return itens_equipamento	

#verifica a frequencia de nomes do item e retorna 4xitem1 3xitem2
def frequenciaItens(itens_equipamento):
	itens = []

	for item in itens_equipamento:
		itens.append(item.nome)
	
	itens_equipamento = {}
	itens_equipamento = {item:itens.count(item) for item in itens}
	print (itens_equipamento)

	itens = []
	for k,v in itens_equipamento.items():
		item = str(v) + 'x' + k
		itens.append(item)

	return itens

def pdf_view(request, *args, **kwargs):
		equipamentos = Equipamento.objects.all()

		data = {
			"patrimonio":equipamentos[0].patrimonio_itti,
			"quantidade":equipamentos[0].id_item.quantidade,
			"itens":frequenciaItens(itens_equipamento(equipamentos[0].id_item.id_item)),
			"equipamento":equipamentos[0].id_item,
			"usuario":"NOME DO COLABORADOR",
			"cpf":"123.123.123-12",
			"date": datetime.datetime.now(),
			"tecnico":"NOME DO FUC. RESP"
		}
		equipamento_dict = {entry for entry in equipamentos}
		pdf = render_to_pdf('controles/pdf_template_exemplo.html', data)
		return HttpResponse(pdf, content_type = 'application/pdf')


def DownloadPDF(request, *args, **kwargs):
	pdf = render_to_pdf('controles/pdf_template.html', data)
	response = HttpResponse(pdf, content_type='application/pdf')
	extension = '.pdf'
	filename = "Invoice_%s" %("12341231")+extension
	content = "attachment; filename = %s"%(filename)
	response['Content-Disposition'] = content
	return response



######################### CATEGORIA ###########################


# Create your views here.
def categorias(request):
	""" Mostra todos os departamentos """
	categorias = Categoria.objects.all().order_by('nome')
	subcategorias = Subcategoria.objects.all()

	context = {'categorias': categorias, 'subcategorias': subcategorias}
	return render(request, 'controles/categorias.html', context)


@login_required
def delete_categoria(request, categoria_id):
	categoria = Categoria.objects.get(id=categoria_id)
	context={'object':'','error':'','itens':''}
	context['object'] = categoria
	try:
		if request.method =="POST":
			categoria.delete()
			return render(request,'controles/categoria/categoria_success.html',context)
		
	except IntegrityError as e:
		print("erro",e)
		itens = Item.objects.all().filter(categoria=categoria_id)
		context['itens'] = itens
		context['error'] = 'Essa categoria está referenciada a algum item. Por favor edite os itens com essa categoria!'
		print(itens)
		print(render_to_string('controles/categoria_confirm_delete.html',context))
		response = JsonResponse({"error": render_to_string('controles/categoria_confirm_delete.html',context)})
		response.status_code = 404
		return response
		#return HttpResponseRedirect(reverse('controles:categorias'))

	return render(request,'controles/categoria_confirm_delete.html',context)
	

@login_required
def nova_categoria(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = CategoriaForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = CategoriaForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:categorias'))

	context = {'form':form}
	return render(request, 'controles/categoria/nova_categoria_modal.html', context)

@login_required
def editar_categoria(request, categoria_id):
	"""Editar um departamento existente """
	categoria = Categoria.objects.get(id=categoria_id)

	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		form = CategoriaForm(instance=categoria)
	else:
		#Dados de POST submetidos; processa os dados
		form = CategoriaForm(instance=categoria, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:categorias'))
	context = {'categoria': categoria, 'form': form}
	return render (request, 'controles/categoria/editar_categoria_modal.html', context)



########################## SUBCATEGORIA ############################


@login_required
def nova_subcategoria(request, categoria_id):
	"""Adiciona um novo departamento"""
	categoria =Categoria.objects.get(id=categoria_id)

	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = SubcategoriaForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = SubcategoriaForm(request.POST)
		if form.is_valid():
			nova_subcategoria=form.save(commit=False)
			nova_subcategoria.categoria = categoria
			nova_subcategoria.save()
			return HttpResponseRedirect(reverse('controles:categorias'))

	context = {'categoria':categoria,'form':form}

	return render(request, 'controles/nova_subcategoria.html', context)



@login_required
def delete_subcategoria(request, subcategoria_id):
	subcategoria = Subcategoria.objects.get(id=subcategoria_id)
	try:
		subcategoria.delete()

	except IntegrityError as e:
		print(e)
		response = JsonResponse({"error":e})
		response.status_code = 404
		return response

	return HttpResponseRedirect(reverse('controles:categorias'))



############################ NOTA FISCAL ######################################

@login_required
def notasfiscais(request):
	""" Mostra todos os departamentos """
	notasfiscais = NotaFiscal.objects.all()
	context = {'notasfiscais': notasfiscais}
	return render(request, 'controles/notasfiscais.html', context)


@login_required
def nova_notafiscal(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = NotaFiscalForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = NotaFiscalForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:notasfiscais'))

	context = {'form':form}
	return render(request, 'controles/nova_notafiscal.html', context)


class NotaFiscalDelete(DeleteView):
	model = NotaFiscal
	success_url = reverse_lazy('controles:notasfiscais')


@login_required
def delete_notafiscal(request, notafiscal_id):
	notafiscal = NotaFiscal.objects.get(id=notafiscal_id)
	context={'object':notafiscal,'error':'','itens':''}
	try:
		if request.method =="POST":
			notafiscal.delete()
			return HttpResponseRedirect(reverse("controles:notasfiscais"))
		
	except IntegrityError as e:
		print("erro",e)
		itens = Item.objects.all().filter(id_notafiscal=notafiscal.id)
		context['itens'] = itens
		print(itens)
		#messages.warning(request, "You can't delete this because it's being used by grupos")
		#return JsonResponse(erros)
	
	return render(request,'controles/notafiscal_confirm_delete.html',context)


########################## Manual ##################################

@login_required
def manuais(request):
	""" Mostra todos os departamentos """
	manuais = Manual.objects.all()
	context = {'manuais': manuais}
	return render(request, 'controles/manuais.html', context)


@login_required
def novo_manual(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = ManualForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = ManualForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:manuais'))

	context = {'form':form}
	return render(request, 'controles/novo_manual.html', context)



@login_required
def delete_manual(request, manual_id):
	manual = Manual.objects.get(id=manual_id)
	manual.delete()
	return HttpResponseRedirect(reverse('controles:manuais'))


############################### ITEM #################################

@login_required
def itens(request):
	""" Mostra todos os departamentos """
	itens = Item.objects.all().order_by('id_item')
	equipamentos = {equipamento.id_item.id_item:equipamento for equipamento in Equipamento.objects.all()}
	print(equipamentos)
	context = {'itens': itens,'equipamentos':equipamentos}
	
	return render(request, 'controles/itens.html', context)


	
def itensByName(request):
	""" Mostra todos os departamentos """
	itens = Item.objects.all().order_by('nome')
	context = {'itens': itens}
	return render(request, 'controles/itens.html', context)



@login_required
def novo_item(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = ItemForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:itens'))

	context = {'form':form}
	return render(request, 'controles/novo_item.html', context)


@login_required
def novo_item_modal(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = ItemForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = ItemForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:itens'))

	context = {'form':form}
	return render(request, 'controles/novo_item_modal.html', context)

@login_required
def duplicar_item_modal(request, item_id):
	"""Editar um departamento existente """
	item = Item.objects.get(id_item=item_id)
	item.id_item = None
	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		form = ItemForm(instance=item)
	else:
		#Dados de POST submetidos; processa os dados
		form = ItemForm(instance=item, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:itens'))
	context = {'item': item, 'form': form}
	return render (request, 'controles/duplicar_item_modal.html', context)



@login_required
def load_subcategorias(request):
    id_categoria = request.GET.get('id_categoria')
    subcategorias = Subcategoria.objects.filter(categoria=id_categoria).order_by('nome')
    return render(request, 'controles/subcategorias_dropdown_list_options.html', {'subcategorias': subcategorias})	

@login_required
def delete_item(request, item_id):
	item = Item.objects.get(id_item=item_id)
	try:
		item.delete()
	except ProtectedError:
		error_message = "This object can't be deleted!!"

	return HttpResponseRedirect(reverse('controles:itens'))

@login_required
def editar_item(request, item_id):
	"""Editar um departamento existente """
	item = Item.objects.get(id_item=item_id)
	print(item)
	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		form = ItemForm(instance=item)
	else:
		#Dados de POST submetidos; processa os dados
		form = ItemForm(instance=item, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:itens'))
	context = {'item': item, 'form': form}
	return render (request, 'controles/editar_item.html', context)

@login_required
def editar_item_modal(request, item_id):
	"""Editar um departamento existente """
	item = Item.objects.get(id_item=item_id)
	print(item)
	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		form = ItemForm(instance=item)
	else:
		#Dados de POST submetidos; processa os dados
		form = ItemForm(instance=item, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('controles:itens'))
	context = {'item': item, 'form': form}
	return render (request, 'controles/editar_item_modal.html', context)	


@login_required
def load_itens_equipamento(request):
	id_item = request.GET.get('id_item')
	itens = Item.objects.filter(id_equipamento_pertencente=id_item).order_by('nome')
	itens_equipamento = []
	for item in itens:
		if (int(item.id_item)!=int(id_item)):
			itens_equipamento.append(item)
	return render(request, 'controles/itens_equipamento.html', {'itens_equipamento': itens_equipamento})	


##########################  VIEWS EQUIPAMENTO ##########################

#Listar
@login_required
def equipamentos(request):
	""" Mostra todos os equipamentos """
	equipamentos = Equipamento.objects.all().order_by('id_item')
	context = {'equipamentos': equipamentos}
	return render(request, 'controles/equipamento/equipamentos.html', context)	


#Cadastro
@login_required
def novo_equipamento(request):
	"""Cadastra NOVO equipamento"""
	"""Aqui gera o id do equipamento e cria o item referente ao equipamento"""

	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		equipamento_form = EquipamentoForm(prefix='equipamento')
		item_form = ItemEquipamentoForm(prefix='item')
	else:
		#Dado de POST EquipamentoForm; processa os dados
		equipamento_form = EquipamentoForm(request.POST, prefix='equipamento')
		item_form = ItemEquipamentoForm(request.POST, prefix='item')

		#Verifica se foi corretamente cadastrado
		if all([equipamento_form.is_valid(), item_form.is_valid()]):

			novo_equipamento = equipamento_form.save(commit=False)
			
			#Cria o item no banco
			item = item_form.save()
	
			#Atualiza equipamento pertencente é ele mesmo
			item.id_equipamento_pertencente = item

			#Atualiza no banco
			item.save()

			#Atualiza id item do equipamento (equipamento é um item)
			novo_equipamento.id_item = item

			#Gera patrimonio itti
			novo_equipamento.patrimonio_itti = gerar_patrimonio_itti(item)
			
			#salva no banco
			novo_equipamento.save()
			
			return HttpResponseRedirect(reverse('controles:equipamentos'))

	context = {'form1':equipamento_form,'form2':item_form}

	return render(request, 'controles/equipamento/novo_equipamento_modal.html', context)

#Gera ID ITTI
def gerar_patrimonio_itti(item):
	'''Gera o Código do Patrimonio do ITTI'''
	'''O Código é formado Pelo Projeto - Ano - Categoria - NUMERO'''
	'''Esse NUMERO é o ID de acordo com os equipamentos que se encaixam em PROJETO-ANO-CATEGORIA'''

	#Obtem OS equipamentoS ITTI em ordem descendente de mesmo - PROJETO - ANO - CATEGORIA
	equipamentos = Equipamento.objects.filter(id_item__categoria__pk=item.categoria.pk).filter(id_item__ano__contains=item.ano).filter(id_item__projeto__pk=item.projeto.pk).order_by('-patrimonio_itti')
	
	#Verifica se existem equipamentos 
	if(equipamentos):
		# Caso SIM - pega o NUMERO do ultimo equipamento cadastrado do mesmo PROJETO-ANO-CATEGORIA
		num = int(equipamentos[0].patrimonio_itti[-6:-3])
	else:
		# Caso NAO - inicia o número
		num = 0
	#FORMATA NUMERO - para 001, 032 
	num_str = "000" + str(num+1)

	#Cria Código patrimonio itti - ACRONIMOPROJETO-CATEG000/00
	patrimonio_itti = item.projeto.acronimo + '-' + item.categoria.abreviacao + num_str[-3:] + '/' + str(item.ano)[-2:]

	return patrimonio_itti


@login_required
def editar_equipamento_modal(request, item_id):
	"""Editar um departamento existente """
	item = Item.objects.get(id_item=item_id)
	equipamento = Equipamento.objects.get(id_item=item_id)

	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		#form = ItemForm(instance=item)
		equipamento_form = EquipamentoForm(prefix='equipamento', instance=equipamento)
		item_form = ItemEquipamentoForm(prefix='item', instance=item)
	else:
		#Dado de POST EquipamentoForm; processa os dados
		equipamento_form = EquipamentoForm(instance=equipamento, data=request.POST, prefix='equipamento')
		item_form = ItemEquipamentoForm(instance=item, data=request.POST, prefix='item')

		if all([equipamento_form.is_valid(), item_form.is_valid()]):
			item=item_form.save()
			equipamento.save()

			return HttpResponseRedirect(reverse('controles:equipamentos'))
	context = {'item': item, 'form1':equipamento_form,'form2':item_form}
	return render (request, 'controles/equipamento/editar_equipamento_modal.html', context)	


@login_required
def delete_equipamento(request, equipamento_id):
	equipamento = Equipamento.objects.get(id_item=equipamento_id)
	context={'object':'','error':'','itens':''}
	context['object'] = equipamento
	try:
		if request.method =="POST":
			item = Item.objects.get(id_item=equipamento_id)

			equipamento.delete()
			item.delete()
			return render(request,'controles/equipamento/equipamento_success.html',context)		
		
	except ProtectedError:
		error_message = "This object can't be deleted!!"
		print(error_message)
		response = JsonResponse({"error": render_to_string('controles/equipamento/equipamento_confirm_delete.html',context)})
		response.status_code = 404
		return response

	return render(request,'controles/equipamento/equipamento_confirm_delete.html',context)



@login_required
def etiqueta(request, equipamento_id):
	'''Gera a Etiqueta do ITTI'''

	#Obtem o equipamento
	equipamento = Equipamento.objects.get(id_item=equipamento_id)
	#Gera 'ACRONIMO PROJETO' / 'ANO'
	texto1 = equipamento.id_item.projeto.acronimo +'/'+str(equipamento.id_item.ano)[2:]

	#Pega o tamanho str do acronimo do projeto
	tam_acron = len(equipamento.id_item.projeto.acronimo)+1

	#Pega apenas 'CATEG000' de ACRONIMO-CATEG000/ANO 
	texto2 = equipamento.patrimonio_itti[tam_acron:-3]

	#Pega patrimonio UFPR
	texto3 = equipamento.patrimonio_ufpr

	#Cria dicionario para o template
	context = {'texto2': texto2, 'texto1':texto1, 'texto3':texto3}

	#Manda renderizar a etiqueta
	return render (request, 'controles/etiqueta/etiqueta.html', context)