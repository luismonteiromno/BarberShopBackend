from django.db import models
from django.core.validators import ValidationError


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
    owner = models.ForeignKey('users.UserProfile', verbose_name='Dono(a)', related_name='owner_barber', null=True, on_delete=models.CASCADE)
    name = models.CharField("Nome da Barbearia", max_length=155, null=False, blank=False)
    phone = models.CharField("Telefone", max_length=15)
    cep = models.CharField("Cep", max_length=12,)
    city = models.CharField("Cidade", max_length=60)
    neighborhood = models.CharField("Bairro", max_length=60)
    state = models.CharField("Estado", max_length=60, default="")
    street = models.CharField("Rua e número", max_length=150)
    instagram_link = models.URLField("Link do instagram", max_length=250)
    facebook_link = models.URLField("Link do facebook", max_length=250)
    business_hours = JSONField(blank=True, null=True, verbose_name='Horário de Funcionamento')

    def clean(self):
        if self.business_hours:
            for opening_hours in self.business_hours:
                days = opening_hours.get('days', [])
                times = opening_hours.get('times', [])
                if not days or not times:
                    raise ValidationError('Os dias e horários de funcionamento devem ser fornecidos.')
                for day in days:
                    if day not in [choice[0] for choice in self.DAY_CHOICES]:
                        raise ValidationError(f'O dia "{day}" não é válido.')


    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name = "Barbearia"
        verbose_name_plural = "Barbearias"


class Schedules(models.Model):
    client = models.ForeignKey('users.UserProfile', verbose_name='Cliente', related_name='client_schedules', on_delete=models.CASCADE)
    date = models.DateTimeField('Horário agendado')
    confirmed_by_barber = models.BooleanField('Agendamento confirmado pelo barbeiro?', default=True)

    def __str__(self):
        return str(self.client)

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'
