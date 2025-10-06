from django.contrib import admin
from .models import user_info

@admin.register(user_info)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'sex', 'photo', 'birthd', 'preview']