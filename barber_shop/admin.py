from django.contrib import admin
from .models import Company, Schedules, Days
from django import forms
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.template import loader
from xhtml2pdf import pisa


class DaysInline(admin.TabularInline):
    model = Days
    fields = ['day', 'hours_business']


class CompanyAdmin(admin.ModelAdmin):
    fieldsets = (
         ('Informações de Contato', {'fields': ('owner', 'employees', 'name', 'phone', 'instagram_link', 'facebook_link')}),
         ('Informações de Endereço', {'fields': ('cep', 'state', 'city', 'neighborhood', 'street')}),
         ('Horário', {'fields': ('opening_hours',)}),
                 )
    inlines = [
        DaysInline
    ]
    filter_horizontal = ['owner', 'employees']


class FormSchedules(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FormSchedules, self).__init__(*args, **kwargs)

        request = self.Meta.formfield_callback.keywords['request']
        user = request.user
        if user.type == 'barbeiro' or user.type == 'desenvolvedor_dono':
            self.fields['confirmed_by_barber'].disabled = False
        else:
            self.fields['confirmed_by_barber'].disabled = True


class SchedulesAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'chosen_barber', 'date', 'confirmed_by_barber']
    list_filter = ['confirmed_by_barber']
    form = FormSchedules
    actions = ['export_as_pdf']

    @admin.action(description='Exportar Selecionados para PDF')
    def export_as_pdf(self, obj, queryset):
        context = {
            "schedules": queryset
        }

        response = HttpResponse(content_type='schedules/pdf')
        response['Content-Disposition'] = 'attachment; filename="schedules.pdf"'

        template = loader.get_template('schedules.html')
        html = template.render(context)

        create_pdf = pisa.CreatePDF(html, dest=response)

        if create_pdf.err:
            raise ValidationError("Problema ao gerar PDF")

        return response


admin.site.register(Company, CompanyAdmin)
admin.site.register(Schedules, SchedulesAdmin)
