from django.contrib import admin
from .models import Company, Schedules


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('owner', 'employees', 'name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
         ('Horário', {'fields': ('opening_hours',)}),
                 )

    filter_horizontal = ['owner', 'employees']


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['client', 'chosen_barber', 'date', 'confirmed_by_barber']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
