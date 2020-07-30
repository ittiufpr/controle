from django import forms

from .models import Departamento, Projeto

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		fields = ['nome']
		labels = {'nome':''}


class ProjetoForm(forms.ModelForm):
	class Meta:
		model = Projeto
		fields = ['nome','acronimo']
