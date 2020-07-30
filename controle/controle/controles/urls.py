
from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from .import views

app_name = "controles"

urlpatterns = [

	url(r'^categorias/$', views.categorias, name='categorias'),
	url(r'^nova_categoria/$', views.nova_categoria, name='nova_categoria'),
	url(r'^editar_categoria/(?P<categoria_id>\d+)/$', views.editar_categoria, name='editar_categoria'),

	url(r'^nova_subcategoria/(?P<categoria_id>\d+)$', views.nova_subcategoria, name='nova_subcategoria'),
	url(r'^delete_subcategoria/(?P<subcategoria_id>\d+)$', views.delete_subcategoria, name='delete_subcategoria'),

	url(r'^notasfiscais/$', views.notasfiscais, name='notasfiscais'),
	url(r'^nova_notafiscal/$', views.nova_notafiscal, name='nova_notafiscal'),
	url(r'^delete_notafiscal/(?P<notafiscal_id>\d+)$', views.delete_notafiscal, name='delete_notafiscal'),

	url(r'^manuais/$', views.manuais, name='manuais'),
	url(r'^novo_manual/$', views.novo_manual, name='novo_manual'),
	url(r'^delete_manual/(?P<manual_id>\d+)$', views.delete_manual, name='delete_manual'),

	#pdf
	url(r'^pdf_view/$', views.pdf_view, name='pdf_view'),
	url(r'^downloadpdf/$', views.DownloadPDF, name='downloadpdf'),


	#itens
	url(r'^itens/$', views.itens, name='itens'),
	url(r'^novo_item/$', views.novo_item, name='novo_item'),
	url(r'^editar_item/(?P<item_id>\d+)/$', views.editar_item, name='editar_item'),
	url(r'^delete_item/(?P<item_id>\d+)$', views.delete_item, name='delete_item'),

	url('ajax/load_subcategorias/', views.load_subcategorias, name='load_subcategorias'),
	url('ajax/load_itens_equipamento/', views.load_itens_equipamento, name='load_itens_equipamento'),

	#equipamento
	url(r'^equipamentos/$', views.equipamentos, name='equipamentos'),
	url(r'^novo_equipamento/', views.novo_equipamento, name='novo_equipamento'),
	url(r'^delete_equipamento/(?P<equipamento_id>\d+)$', views.delete_equipamento, name='delete_equipamento'),

	url(r'^ajax/itensByName/$', views.itensByName, name='itensByName'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)