from django.contrib import admin

from .models import (
    Administration,
)


class AdministrationAdmin(admin.ModelAdmin):
    search_fields = ["uuid", "nom", "code"]
    list_display = ["uuid", "nom", "code", "ville_signature"]


admin.site.register(Administration, AdministrationAdmin)
