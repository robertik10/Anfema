from django.db import models


# model für daten aus der JSON Datei https://www.anfe.ma/api/v2/projects/?format=json&locale=en
class AnfemaPorject(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=200)
    meta_first_published_at = models.DateTimeField("date published")
    client = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=200)
    brand_main_colour = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now = True) # auto_now = True -> wird bei jedem speichern aktualisiert
     
    def __str__(self):
        return self.title
    
