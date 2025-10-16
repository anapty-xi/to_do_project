from django.contrib import admin
from .models import Todo


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'name', 'publish_date', 'status',]
    prepopulated_fields = {"slug": ["name"]}