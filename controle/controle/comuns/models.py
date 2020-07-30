from django.db import models

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