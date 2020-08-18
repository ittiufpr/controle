
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from .import views

app_name = "comuns"

urlpatterns = [
	url(r'^$', views.index, name='index'),

	#Página mostra departamentos
	url(r'^departamentos/$', views.departamentos, name='departamentos'),
	#Página para adicionar novos departamentos
	url(r'^novo_departamento/$', views.novo_departamento, name='novo_departamento'),
	#Edita um departamento
	url(r'^editar_departamento/(?P<departamento_id>\d+)/$', views.editar_departamento, name='editar_departamento'),

	url(r'^delete_departamento/(?P<departamento_id>\d+)$', views.delete_departamento, name='delete_departamento'),

	#Mostra projetos
	url(r'^projetos/$', views.projetos, name='projetos'),
	#mostra Formulario para cadastro de projetos
	url(r'^novo_projeto/$', views.novo_projeto, name='novo_projeto'),
	#Mostra formulario para editar projetos
	url(r'^editar_projeto/(?P<projeto_id>\d+)/$', views.editar_projeto, name='editar_projeto'),

	#Mostra Pessoas
	url(r'^pessoas/$', views.pessoas, name='pessoas'),
	url(r'^editar_pessoa/(?P<pessoa_cpf>\d+)/$', views.editar_pessoa, name='editar_pessoa'),
	url(r'^nova_pessoa/$', views.nova_pessoa, name='nova_pessoa'),
	url(r'^delete_pessoa/(?P<pessoa_cpf>\d+)$', views.delete_pessoa, name='delete_pessoa'),
]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)