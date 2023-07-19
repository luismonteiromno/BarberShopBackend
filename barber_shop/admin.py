from django.contrib import admin
from .models import Company, Schedules


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('owner', 'name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
         ('Horário', {'fields': ('opening_hours',)}),
                 )

    #list_display = ['id', 'name']
    #search_fields = ['name']


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'confirmed_by_barber']
    readonly_fields = ['date']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
