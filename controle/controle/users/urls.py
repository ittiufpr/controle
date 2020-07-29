from django.conf.urls import url
from django.contrib.auth.views import LoginView
from django.urls import path
from .import views

app_name = "users"

urlpatterns = [
	#Página de login
	path('login/',  LoginView.as_view(template_name='users/login.html'), name="login"),
	url(r'^logout/$', views.logout_view, name='logout'),
]
