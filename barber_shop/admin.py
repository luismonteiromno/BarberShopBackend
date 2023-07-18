from django.contrib import admin
from .models import Company, Schedules


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
         ('Horário', {'fields': ('business_hours',)}),
                 )

    readonly_fields = ('formatted_business_hours',)
    def formatted_business_hours(self, obj):
        if obj.business_hours:
            formatted_hours = []
            for opening_hours in obj.business_hours:
                days = opening_hours.get('days', [])
                times = opening_hours.get('times', [])
                hours_str = ', '.join(f"{day}: {time}" for day, time in zip(days, times))
                formatted_hours.append(hours_str)
            return ', '.join(formatted_hours)
        return ''

    formatted_business_hours.short_description = 'Horário de Funcionamento'
    #list_display = ['id', 'name']
    #search_fields = ['name']


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['client', 'date', 'confirmed_by_barber']
    readonly_fields = ['date']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
