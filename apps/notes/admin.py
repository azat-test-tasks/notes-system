from django.contrib import admin

from apps.notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "title", "description", "created_at")
    list_display_links = ("id", "title")
    search_fields = ("title", "description")
    list_filter = ("created_at",)
    readonly_fields = ("id", "created_at")
