from django.contrib import admin
from .models import CustomUser

# Register your models here.

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'is_superuser']
    search_fields = ['full_name']

