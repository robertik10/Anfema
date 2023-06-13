from django.shortcuts import render
from django.http import HttpResponse
from . models import AnfemaPorject


# Create your views here.
def last_update(request):
    
    return HttpResponse("Hello, world. You're at the polls index.")
    