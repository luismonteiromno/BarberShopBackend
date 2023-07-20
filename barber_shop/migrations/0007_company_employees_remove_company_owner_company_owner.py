# Generated by Django 4.2.3 on 2023-07-19 16:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('barber_shop', '0006_company_opening_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='employees',
            field=models.ManyToManyField(related_name='employees_barber', to=settings.AUTH_USER_MODEL, verbose_name='Funcionários'),
        ),
        migrations.RemoveField(
            model_name='company',
            name='owner',
        ),
        migrations.AddField(
            model_name='company',
            name='owner',
            field=models.ManyToManyField(related_name='owner_barber', to=settings.AUTH_USER_MODEL, verbose_name='Dono(a)'),
        ),
    ]