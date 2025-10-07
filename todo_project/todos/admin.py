from django.contrib import admin
from .models import todo


@admin.register(todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'publish_date', 'active',]
    prepopulated_fields = {"slug": ["name"]}