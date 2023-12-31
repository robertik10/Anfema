from django.contrib import admin
from .models import AnfemaProject


class AnfemaProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'meta_first_published_at', 'client', 'subtitle', 'brand_main_colour', 'updated_at')

# Register your models here.
admin.site.register(AnfemaProject, AnfemaProjectAdmin)