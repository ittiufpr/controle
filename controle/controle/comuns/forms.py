from django import forms

from .models import Departamento, Projeto, Pessoa

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

class DepartamentoForm(forms.ModelForm):
	class Meta:
		model = Departamento
		fields = ['nome']
		labels = {'nome':''}


class ProjetoForm(forms.ModelForm):
	class Meta:
		model = Projeto
		fields = ['nome','acronimo']

class PessoaForm(forms.ModelForm):
	class Meta:
		model = Pessoa
		fields = ['cpf','nome', 'email']

	def clean_cpf(self):
		cpf = self.cleaned_data['cpf']

		#check se cpf não contem letras 
		if not cpf.isnumeric() :
			raise ValidationError(_('Por favor digite apenas NUMEROS [0-9]! '))

		return cpf