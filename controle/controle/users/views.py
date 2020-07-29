from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.http import HttpResponseRedirect

from django.contrib.auth import logout

def logout_view(request):
	"""Faz logout do usuário."""
	logout(request)
	return HttpResponseRedirect(reverse('controles:departamentos'))