from django import template

from django.conf import settings
import os



register = template.Library()

@register.filter(name = 'status')
def status(value): # Only one argument.
    """Converts a string into all lowercase"""
    if value:
    	path = os.path.join(settings.MEDIA_URL,"img/verde.png" )
    	return path
    else:
    	path = os.path.join(settings.MEDIA_URL,"img/preto.png" )
    	return path
