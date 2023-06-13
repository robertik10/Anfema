from django.shortcuts import render
from . models import AnfemaPorject
from django.http import JsonResponse

# returns last updated entry as JSON file
def last_update(request):
    return JsonResponse(AnfemaPorject.objects.latest('updated_at').as_dict())
    