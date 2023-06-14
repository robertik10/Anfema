from . models import AnfemaProject
from django.http import JsonResponse
from django.http import HttpResponse
from . tasks import celery_perform_update

# returns title of last updated entry as JSON file
def last_update(self):
    try:
        last_update = AnfemaProject.objects.latest('updated_at')
    except AnfemaProject.DoesNotExist:
        return JsonResponse({"!database empty!":"no entries found"})
        
    print(last_update)
    response = JsonResponse({"last updated entry title":str(last_update)})
    return response

# loads data from url and saves it to database
# if optional header "X-OLDER_THAN datum zeit" is set => only save entries that are older than the given date
def perform_update(request):
    request_method = request.method
    url = 'https://www.anfe.ma/api/v2/projects/?format=json&locale=en'
    
    # if request is not a POST request => return 405 Status Code
    if request_method != "POST":
        return HttpResponse("This request has to be a POST request! Instead it was a {} request".format(request_method), status = 405)
    
    # let celery task perform the rest:
    celery_perform_update(request, url)  
    #celery_perform_update.delay(request, url)
    return HttpResponse("Request accepted. Data is being processed from {} and saved to database".format(url), status = 202)