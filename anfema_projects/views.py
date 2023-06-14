from django.shortcuts import render
from . models import AnfemaPorject
from django.http import JsonResponse
from django.http import HttpResponse
import requests
import json
import datetime

# returns title of last updated entry as JSON file
def last_update(self):
    try:
        last_update = AnfemaPorject.objects.latest('updated_at')
    except AnfemaPorject.DoesNotExist:
        return JsonResponse({"!database empty!":"no entries found"})
        
    print(last_update)
    response = JsonResponse({"last updated entry title":str(last_update)})
    return response

# loads data from url and saves it to database
# if optional header "X-OLDER_THAN datum zeit" is set => only save entries that are older than the given date
def perform_update(request):
    request_method = request.method
    url = 'https://www.anfe.ma/api/v2/projects/?format=json&locale=en'
    header_date = None
    
    # if request is not a POST request => return 405 Status Code
    if request_method != "POST":
        return HttpResponse("This request has to be a POST request! Instead it was a {} request".format(request_method), status = 405)
    # check if "X-OLDER_THAN datum zeit" header was added and set header_check to True if it was
    if request.headers.get("X-OLDER_THAN") != None:
        header_date = request.headers.get("X-OLDER_THAN")
        
    # if request is a POST request => load data from url and save it to database
    r = requests.get(url)
    # check if data was successfully loaded from url
    if r.status_code != 200:
        return HttpResponse("Error while loading data from {}".format(url), status = 500)
    
    
    # preparing and saving data to database
    data = json.loads(r.content)

    items = data['items']
    for project in items:
        # if header_date is not None => check if project['meta']['first_published_at'] is older than header_date
        # skip this project if it is newer than header_date
        if header_date != None:
            if project['meta']['first_published_at'] >= header_date:
                continue
        id = project['id']
        title = project['title']
        meta_first_published_at = project['meta']['first_published_at']
        client = project['client']
        subtitle = project['subtitle']
        brand_main_colour = project['brand_main_colour']
        
        anfema_project = AnfemaPorject(id=id, title=title, meta_first_published_at=meta_first_published_at, client=client, subtitle=subtitle, brand_main_colour=brand_main_colour)
        anfema_project.save()
        
    
    return HttpResponse("Data successfully loaded from {} and saved to database".format(url), status = 200)