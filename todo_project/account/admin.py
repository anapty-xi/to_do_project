from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'sex', 'photo', 'birthd', 'preview']