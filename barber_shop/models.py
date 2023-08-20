from django.db import models
from django.core.validators import ValidationError
from django.contrib.postgres.fields import ArrayField

try:
    from django.db.models import JSONField
except ImportError:
    from django.contrib.postgres.fields import JSONField


class Company(models.Model):
    DAY_CHOICES = [
        ('seg', 'Segunda-feira'),
        ('ter', 'Terça-feira'),
        ('qua', 'Quarta-feira'),
        ('qui', 'Quinta-feira'),
        ('sex', 'Sexta-feira'),
        ('sab', 'Sábado'),
        ('dom', 'Domingo'),
    ]
    owner = models.ManyToManyField('users.UserProfile', verbose_name='Dono(a)', related_name='owner_barber')
    employees = models.ManyToManyField('users.UserProfile', verbose_name='Funcionários', related_name='employees_barber', blank=True)
    name = models.CharField("Nome da Barbearia", max_length=155, null=False, blank=False)
    phone = models.CharField("Telefone", max_length=15)
    cep = models.CharField("Cep", max_length=12,)
    city = models.CharField("Cidade", max_length=60)
    neighborhood = models.CharField("Bairro", max_length=60)
    state = models.CharField("Estado", max_length=60, default="")
    street = models.CharField("Rua e número", max_length=150)
    instagram_link = models.URLField("Link do instagram", max_length=250, blank=True, null=True)
    facebook_link = models.URLField("Link do facebook", max_length=250, blank=True, null=True)
    whatsapp_link = models.URLField("Link do whatsapp", max_length=250, blank=True, null=True)
    business_hours = JSONField(blank=True, null=True, verbose_name='Horário de Funcionamento')
    opening_hours = ArrayField(models.CharField(max_length=255), null=True, verbose_name='Horário de Funcionamento')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Barbearia"
        verbose_name_plural = "Barbearias"


class Days(models.Model):
    day = models.CharField('Dia', max_length=50)
    start = models.TimeField('Horário de inicio', null=True, auto_created=True)
    end = models.TimeField('Horário de encerramento', null=True, auto_created=True)
    pause_time = models.TimeField('Horário de pausa', blank=True, null=True, help_text='(opcional)')
    end_pause_time = models.TimeField('Fim da pausa', blank=True, null=True, help_text='(opcional)')
    working_day = models.BooleanField('Dia de funcionamento', default=True)
    company = models.ForeignKey(Company, verbose_name='Barbearia', null=True, blank=True, related_name='company_dat', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = 'Dia'
        verbose_name_plural = 'Dias de Funcionamento'


class Schedules(models.Model):
    barbershop = models.ForeignKey(Company, verbose_name='Barbearia', on_delete=models.PROTECT)
    day = models.ForeignKey(Days, verbose_name='Dia', related_name='schedules_days', on_delete=models.PROTECT)
    client = models.ForeignKey('users.UserProfile', verbose_name='Cliente', related_name='client_schedules', on_delete=models.CASCADE)
    date = models.DateTimeField('Horário agendado')
    chosen_barber = models.ForeignKey('users.UserProfile', verbose_name='Barbeiro escolhido pelo cliente', related_name='client_chosen_barber', on_delete=models.CASCADE, null=True)
    confirmed_by_barber = models.BooleanField('Agendamento confirmado pelo barbeiro?', blank=True, null=True, default=False, help_text='Aguarde até o barbeiro confirmar o agendamento')
    user_canceled = models.BooleanField('Cancelado pelo usuário?', default=False)

    def __str__(self):
        return str(self.client)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'


class SchedulesDays(models.Model):
    day = models.ForeignKey(Days, verbose_name='Dia', related_name='schedule_day', on_delete=models.PROTECT)
    schedule = models.ForeignKey(Schedules, verbose_name='Agendado por', related_name='schedule', on_delete=models.PROTECT)
    data = models.DateTimeField('Data')

    def __str__(self):
        return f"{self.day} - {self.schedule}"

    class Meta:
        verbose_name = 'Dia agendado'
        verbose_name_plural = 'Dias agendados'
