from django.contrib import admin
from .models import Company, Schedules, Days, SchedulesDays
from django import forms


class DaysInline(admin.StackedInline):
    model = Days
    fields = ['day', 'start', 'end', 'pause_time', 'end_pause_time', 'working_day']


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('owner', 'employees', 'name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
                 )
    inlines = [
        DaysInline
    ]
    filter_horizontal = ['owner', 'employees']
    list_display = ['id', 'name']


class FormSchedules(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSchedules, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']
        user = request.user
        if user.type == 'barbeiro' or user.type == 'desenvolvedor_dono':
            self.fields['confirmed_by_barber'].disabled = False
            self.fields['user_canceled'].disabled = False
        elif user.type == 'cliente':
            self.fields['confirmed_by_barber'].disabled = True
            self.fields['user_canceled'].disabled = False


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'chosen_barber', 'date', 'day', 'confirmed_by_barber', 'user_canceled']
    list_filter = ['confirmed_by_barber']
    form = FormSchedules


class SchedulesDaysAdmin(admin.ModelAdmin):
    list_display = ['id', 'day', 'schedule', 'data']


class DaysAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Modificar dia', {'fields': ('day', 'start', 'end', 'pause_time', 'end_pause_time', 'company', 'working_day')}),
    )
    list_display = ['id', 'day', 'start', 'end', 'company']
    list_filter = ['company']


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
admin.site.register(SchedulesDays, SchedulesDaysAdmin)
admin.site.register(Days, DaysAdmin)
