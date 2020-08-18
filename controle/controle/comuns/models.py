from django.db import models
from cpf_field.models import CPFField

# Create your models here.

class Departamento(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

        
class Projeto(models.Model):
    nome = models.CharField(max_length=30)
    acronimo = models.CharField(max_length=5)
    def __str__(self):
        return self.nome + ' ' + self.acronimo

class Pessoa(models.Model):
	cpf   = CPFField(unique=True, primary_key=True)
	nome  = models.CharField(max_length=80, null = True, blank=False)
	email = models.EmailField(blank=True, null=True)
	def __str__(self):
		return self.cpf + ' ' +self.nome

class Funcionario(models.Model):
	cpf          = models.OneToOneField(Pessoa, primary_key= True, on_delete=models.CASCADE)
	departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, blank=True, null=True)
	funcao       = models.CharField(max_length=50)

