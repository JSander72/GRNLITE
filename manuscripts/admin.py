from django.contrib import admin
from .models import Manuscript


@admin.register(Manuscript)
class ManuscriptAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "status", "created_at", "updated_at")
