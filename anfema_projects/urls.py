from django.urls import path
from . import views

app_name ="anfema_projects"

urlpatterns = [
    path("last-update/", views.last_update, name="last update"),
    path("perform-update/", views.perform_update, name="perform update"),
]