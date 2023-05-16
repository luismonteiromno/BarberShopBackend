from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile

# Register your models here
class UserProfileAdmin(UserAdmin):
    ordering = ['id']
    fieldsets = ('Informações do Usuário', {'fields': ('username', 'owner_company', 'password', 'full_name', 'email')}),

    search_fields = ['email', 'full_name', 'username']
    list_display = ['id', 'email', 'full_name', 'username']
    list_display_links = ['id', 'email']


admin.site.register(UserProfile, UserProfileAdmin)
