from django.db import models
from datetime import datetime

# Create your models here.
# model für daten aus der JSON Datei https://www.anfe.ma/api/v2/projects/?format=json&locale=en
class AnfemaPorject(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    meta_first_published_at = models.DateTimeField("date published")
    client = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    brand_main_color = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now = True, blank=True)  #TODO: why should this be blank?
     
    def __str__(self):
        return self.title
    
