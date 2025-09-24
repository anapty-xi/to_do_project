from django.contrib import admin
from .models import profile_info

@admin.register(profile_info)
class ProfileInfoAdmin(admin.ModelAdmin):
    list_display = ['sex']