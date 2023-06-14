import requests
import json
from celery import shared_task
from . models import AnfemaProject

@shared_task
# loads data from url and saves it to database
# if optional header "X-OLDER_THAN datum zeit" is set => only save entries that are older than the given date
def celery_perform_update(request, url):
    header_date = None
    # check if "X-OLDER_THAN datum zeit" header was added and set header_check to True if it was
    if request.headers.get("X-OLDER_THAN") != None:
        header_date = request.headers.get("X-OLDER_THAN")
        
    # if request is a POST request => load data from url and save it to database
    r = requests.get(url)
    
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
        
        anfema_project = AnfemaProject(id=id, title=title, meta_first_published_at=meta_first_published_at, client=client, subtitle=subtitle, brand_main_colour=brand_main_colour)
        anfema_project.save()