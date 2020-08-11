from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from comuns.models import Departamento, Projeto
import datetime


def current_year():
    return datetime.date.today().year


def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

class Categoria(models.Model):
    nome = models.CharField(max_length=40)
    abreviacao = models.CharField(max_length=4)
    #subcategoria = models.ForeignKey('self', null=True, blank=True ,related_name='categoria', on_delete=models.PROTECT)
    def __str__(self):
        return self.nome

class Subcategoria(models.Model):
    nome = models.CharField(max_length=40)
    categoria = models.ForeignKey(Categoria, null=True, blank=True, on_delete=models.CASCADE)
    def __str__(self):
        return self.categoria.nome + " " + self.nome

class Manual(models.Model):
    nome = models.CharField(max_length=50)
    documento = models.FileField(upload_to='uploads/manual/')
    
    class Meta:
        verbose_name_plural = 'manuais'
    def __str__(self):
        return self.nome
    def delete(self, *args, **kwargs):
        self.documento.delete()
        super().delete(*args, **kwargs)    

class NotaFiscal(models.Model):
    nome = models.CharField(max_length=50)
    documento = models.FileField(upload_to='uploads/notafiscal/')
    class Meta:
        verbose_name_plural = 'notas fiscais'
        
    def __str__(self):
        return self.nome

    def delete(self, *args, **kwargs):
        self.documento.delete()
        super().delete(*args, **kwargs)

    

class Item(models.Model):
    id_item = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=50)
    caracteristica = models.TextField(max_length=200, blank=True, null=True)
    marca = models.CharField(max_length=30) #nova identidade
    modelo = models.CharField(max_length=30) #nova identidade
    categoria = models.ForeignKey(Categoria, on_delete=models.PROTECT)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.PROTECT, blank=True, null=True)
    projeto = models.ForeignKey('comuns.Projeto', on_delete=models.PROTECT)
    valor = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null = True)
    local = models.CharField(max_length=50, null = True, blank=True) #nova identidade
    id_departamento = models.ForeignKey('comuns.Departamento', on_delete=models.PROTECT, blank=True, null = True)
    id_notafiscal = models.ForeignKey(NotaFiscal, on_delete=models.PROTECT, blank=True, null = True)
    status_disponivel = models.BooleanField(default=True)
    status_manutencao = models.BooleanField(default=False)
    status_emprestado = models.BooleanField(default=False)
    tipo_consumivel = models.BooleanField(default=False)
    quantidade = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)], default = 1)
    validade = models.DateField(null= True, blank=True)
    id_equipamento_pertencente = models.ForeignKey('self', null=True, blank=True ,related_name='item', on_delete=models.CASCADE)
    ano = models.PositiveIntegerField(
        default=current_year(), validators=[MinValueValidator(2009), max_value_current_year])

    def __str__(self):
        if(self.tipo_consumivel):
            return self.nome + ' ' + self.categoria.nome  + ' ' + str(self.marca)+' '+str(self.modelo) +' '+ str(self.quantidade)+' '+ str(self.validade) +' '+ self.projeto.acronimo
        else:
            return self.nome + ' ' + self.categoria.nome  + ' ' + str(self.marca)+' '+str(self.modelo) +' '+ self.projeto.acronimo
    
    class Meta:
        verbose_name_plural = 'Itens'

class Equipamento(models.Model):
    '''Representa um equipamento'''
    id_item = models.OneToOneField(Item, primary_key = True, on_delete=models.PROTECT)
    patrimonio_itti = models.CharField(max_length=30, unique=True, blank=True, null= True, default='')
    patrimonio_ufpr = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(999999)] ,unique=True, null= True, blank=True)
    id_manual = models.ForeignKey(Manual, on_delete=models.SET_NULL, blank=True, null = True)


    def __str__(self):
        return str(self.patrimonio_ufpr) + ' ' + str(self.patrimonio_itti)
