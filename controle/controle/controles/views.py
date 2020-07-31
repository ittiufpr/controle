from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

#import Models
from .models import Categoria, Subcategoria, NotaFiscal, Manual, Item, Equipamento

#import Model Comuns
from comuns.models import Projeto, Departamento

from .forms import CategoriaForm, SubcategoriaForm, NotaFiscalForm, ManualForm, ItemForm, EquipamentoForm

#pdf imports
from django.template.loader import get_template, render_to_string
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
from django.views import View

#Erro to delete protected
from django.db.models import ProtectedError

from django.conf import settings
import datetime
import os
import time
from django.db.models.signals import post_save

from django.http import JsonResponse

from django.views.generic.edit import DeleteView
from django.urls import reverse_lazy

data = {
	"patrimonio":'123456',
	"quantidade":1,
	"descricao":'descricao do item',
	"usuario":"NOME DO COLABORADOR",
	"cpf":"123.123.123-12",
	"date": datetime.datetime.now(),
	"tecnico":"NOME DO FUC. RESP"
}



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



def pdf_view(request, *args, **kwargs):
		pdf = render_to_pdf('controles/pdf_template_plaqueta.html', data)
		return HttpResponse(pdf, content_type = 'application/pdf')


def DownloadPDF(request, *args, **kwargs):
	pdf = render_to_pdf('controles/pdf_template.html', data)
	response = HttpResponse(pdf, content_type='application/pdf')
	extension = '.pdf'
	filename = "Invoice_%s" %("12341231")+extension
	content = "attachment; filename = %s"%(filename)
	response['Content-Disposition'] = content
	return response


# Create your views here.
def categorias(request):
	""" Mostra todos os departamentos """
	categorias = Categoria.objects.all().order_by('nome')
	subcategorias = Subcategoria.objects.all()

	context = {'categorias': categorias, 'subcategorias': subcategorias}
	return render(request, 'controles/categorias.html', context)



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
	return render(request, 'controles/nova_categoria.html', context)




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
	subcategoria.delete()
	return HttpResponseRedirect(reverse('controles:categorias'))



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
	return render (request, 'controles/editar_categoria.html', context)



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
	try:
		notafiscal.delete()
		
	except ProtectedError :
		print("erro")

	return HttpResponseRedirect(reverse('controles:notasfiscais'))




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


@login_required
def itens(request):
	""" Mostra todos os departamentos """
	itens = Item.objects.all().order_by('id_item')
	context = {'itens': itens}
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
def load_subcategorias(request):
    id_categoria = request.GET.get('id_categoria')
    subcategorias = Subcategoria.objects.filter(categoria=id_categoria).order_by('nome')
    print("Chegou aqui!", id_categoria)
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
def load_itens_equipamento(request):
	id_item = request.GET.get('id_item')
	itens = Item.objects.filter(id_equipamento_pertencente=id_item).order_by('nome')
	itens_equipamento = []
	for item in itens:
		if (int(item.id_item)!=int(id_item)):
			itens_equipamento.append(item)
	return render(request, 'controles/itens_equipamento.html', {'itens_equipamento': itens_equipamento})	

@login_required
def equipamentos(request):
	""" Mostra todos os equipamentos """
	equipamentos = Equipamento.objects.all().order_by('id_item')
	#for equipamento in equipamentos:
	#	itens_equipamentos = Item.objects.filter(id_equipamento_pertencente=equipamento.id_item).order_by('nome')
	#	for item in itens_equipamentos:
	#		if (item.id_item!=equipamento.id_item.id_item):
	#			print(itens_equipamentos)
	context = {'equipamentos': equipamentos}
	return render(request, 'controles/equipamentos.html', context)	

def save_item(sender, instance, **kwargs):
    print(teste.save())

@login_required
def novo_equipamento(request):
	"""Cadastra novo equipamento"""

	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		equipamento_form = EquipamentoForm(prefix='equipamento')
		item_form = ItemForm(prefix='item')
	else:
		#Dado de POST EquipamentoForm; processa os dados
		equipamento_form = EquipamentoForm(request.POST, prefix='equipamento')
		item_form = ItemForm(request.POST, prefix='item')
		if all([equipamento_form.is_valid(), item_form.is_valid()]):
			novo_equipamento=equipamento_form.save(commit=False)
			#salva instancia do form dos itens no bd
			novo_item = item_form.save()
			#pega a instacia do item armazenado
			item = Item.objects.get(id_item=novo_item.id_item)
			#atualiza id do equipamento (se é equipamento é ele mesmo)
			item.id_equipamento_pertencente = item
			#salva item
			item.save()
			novo_equipamento.id_item = item
			n = item.id_item
			id_itti = "00000" + str(n)
			print(id_itti)
			novo_equipamento.patrimonio_itti = item.projeto.acronimo+id_itti[-5:]
			novo_equipamento.save()
			return HttpResponseRedirect(reverse('controles:equipamentos'))

	context = {'form1':equipamento_form,'form2':item_form}

	return render(request, 'controles/novo_equipamento.html', context)

@login_required
def delete_equipamento(request, equipamento_id):
	equipamento = Equipamento.objects.get(id_item=equipamento_id)
	try:
		equipamento.delete()
	except ProtectedError:
		error_message = "This object can't be deleted!!"
		print(error_message)

	return HttpResponseRedirect(reverse('controles:equipamentos'))