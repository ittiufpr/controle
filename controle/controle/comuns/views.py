from django.shortcuts import render

from .forms import DepartamentoForm
# Create your views here.
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

#Importação de Models
from .models import Departamento, Projeto

#importação de Forms
from .forms import ProjetoForm, DepartamentoForm

def index(request):
	return render(request,'comuns/index.html')

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
		#Requisisção inicial; preenche preciamento o formulário com a entrada atual
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
	return render(request, 'comuns/projetos.html', context)




@login_required
def novo_projeto(request):
	"""Adiciona um novo projeto"""
	if request.method != 'POST':
			#Nenhum dado submetido; cria um formulário em branco
		form = ProjetoForm()
	else:
		#Dado de POST submetidos; processa os dados
		form = ProjetoForm(request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('comuns:projetos'))

	context = {'form':form}

	return render(request, 'comuns/novo_projeto.html', context)


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
	return render (request, 'comuns/editar_projeto.html', context)
