from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UserProfile
from django import forms


class FormUser(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormUser, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']

        if request.user.type == 'desenvolvedor_dono':
            self.fields['type'].disabled = False
        else:
            self.fields['type'].disabled = True


class UserProfileAdmin(UserAdmin):
    ordering = ['id']
    fieldsets = ('Informações do Usuário', {'fields': ('username', 'type', 'owner', 'password', 'full_name', 'email',
                                                       'description', 'image')}),
    form = FormUser
    search_fields = ['email', 'full_name', 'username']
    list_display = ['id', 'email', 'full_name', 'username']
    list_display_links = ['id', 'email']


admin.site.register(UserProfile, UserProfileAdmin)
