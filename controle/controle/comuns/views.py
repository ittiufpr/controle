from django.shortcuts import render

from .forms import DepartamentoForm
# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#Importação de Models
from .models import Departamento, Projeto, Pessoa

#importação de Forms
from .forms import ProjetoForm, DepartamentoForm, PessoaForm


from django.http import HttpResponse
from django.views import View

#Erro to delete protected
from django.db.models import ProtectedError

#Ajax handle
import json
from django.http import JsonResponse

#Erro to delete protected
from django.db.models import ProtectedError
from django.db import IntegrityError
from django.template.loader import render_to_string

def index(request):
	return render(request,'comuns/index.html')

@login_required
# Create your views here.
def departamentos(request):
	""" Mostra todos os departamentos """
	departamentos = Departamento.objects.all().order_by('nome')
	context = {'departamentos': departamentos}
	return render(request, 'comuns/departamentos.html', context)

@login_required
def novo_departamento(request):
	"""Adiciona um novo departamento"""
	if request.method != 'POST':
		#Nenhum dado submetido; cria um formulário em branco
		form = DepartamentoForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = DepartamentoForm(request.POST)
		if form.is_valid():
			print("SALVEI!")
			form.save()
			return HttpResponseRedirect(reverse('comuns:departamentos'))
	context = {'form':form}
	return render(request, 'comuns/novo_departamento.html', context)


@login_required
def delete_departamento(request, departamento_id):
	departamento = Departamento.objects.get(id=departamento_id)
	departamento.delete()
	return HttpResponseRedirect(reverse('comuns:departamentos'))


@login_required
def editar_departamento(request, departamento_id):
	"""Editar um departamento existente """
	departamento = Departamento.objects.get(id=departamento_id)
	
	if request.method !='POST':
		#Requisição inicial; preenche preciamento o formulário com a entrada atual
		form = DepartamentoForm(instance=departamento)
	else:
		#Dados de POST submetidos; processa os dados
		form = DepartamentoForm(instance=departamento, data=request.POST)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect(reverse('comuns:departamentos'))

	context = {'departamento': departamento, 'form': form}
	return render (request, 'comuns/editar_departamento.html', context)



#Projeto Views


@login_required
def projetos(request):
	""" Mostra todos os projetos """
	projetos = Projeto.objects.all()
	context = {'projetos': projetos}
	return render(request, 'comuns/projeto/projetos.html', context)




@login_required
def novo_projeto(request):
	"""Adiciona um novo projeto"""
	data = {}
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = ProjetoForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = ProjetoForm(request.POST)
		if form.is_valid():
			try:
				form.save()
				data['stat'] = "OK";
				return HttpResponse(json.dumps(data), content_type='application/json')
			except IntegrityError as e:
				print(e)
		else:
			context = {'form': form}
			return render(request, 'comuns/projeto/novo_projeto.html', context)

	context = {'form':form}

	return render(request, 'comuns/projeto/novo_projeto.html', context)

	


@login_required
def editar_projeto(request, projeto_id):
	"""Editar um projeto existente """
	projeto = Projeto.objects.get(id=projeto_id)

	if request.method !='POST':
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
		form = ProjetoForm(instance=projeto)
	else:
		#Dados de POST submetidos; processa os dados
		form = ProjetoForm(instance=projeto, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('comuns:projetos'))
	context = {'projeto': projeto, 'form': form}
	return render (request, 'comuns/projeto/editar_projeto.html', context)

########## PESSOAS ##########

@login_required
def pessoas(request):
	""" Mostra todos os departamentos """
	pessoas = Pessoa.objects.all().order_by('nome')
	context = {'pessoas': pessoas}
	return render(request, 'comuns/pessoa/pessoas.html', context)


@login_required
def nova_pessoa(request):
	"""Adiciona um novo projeto"""
	data = {}
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = PessoaForm()
		
	else:
		#Dado de POST submetidos; processa os dados
		form = PessoaForm(request.POST)
		if form.is_valid():
			form.save()
			data['stat'] = "OK";
			return HttpResponse(json.dumps(data), content_type='application/json')

		else:
			context = {'form': form}
			return render(request, 'comuns/pessoa/nova_pessoa.html', context)

	context = {'form':form}

	return render(request, 'comuns/pessoa/nova_pessoa.html', context)


@login_required
def editar_pessoa(request, pessoa_cpf):
	"""Editar um projeto existente """
	pessoa = Pessoa.objects.get(cpf=pessoa_cpf)
	context = {}
	data = {}
	if request.method !='POST':
		#Requisisção inicial; preenche o formulário com a entrada atual
		form = PessoaForm(instance=pessoa)
	else:
		#Dados de POST submetidos; processa os dados
		form = PessoaForm(instance=pessoa, data=request.POST)
		print(form)
		if form.is_valid():
			form.save()
			data['stat'] = "OK";
			return HttpResponse(json.dumps(data), content_type='application/json')

		else:
			context = {'pessoa': pessoa, 'form': form}
			return render (request, 'comuns/pessoa/editar_pessoa.html', context)

	context = {'pessoa': pessoa, 'form': form}
	return render (request, 'comuns/pessoa/editar_pessoa.html', context)



@login_required
def delete_pessoa(request, pessoa_cpf):
	pessoa = Pessoa.objects.get(cpf=pessoa_cpf)
	context={'object':'','error':'','itens':''}
	context['object'] = pessoa
	data = {}
	try:
		if request.method =="POST":
			pessoa.delete()
			data['stat'] = "OK";
			return HttpResponse(json.dumps(data), content_type='application/json')

	except IntegrityError as e:
		print("erro",e)
		repr(e)
		context['error'] = 'Esta pessoa está Referenciada. Por favor resolva as pendências dela antes de fazer essa operação'
		response = JsonResponse({"error": render_to_string('comuns/pessoa/pessoa_confirm_delete.html',context)})
		response.status_code = 404
		return response

	return render(request,'comuns/pessoa/pessoa_confirm_delete.html',context)