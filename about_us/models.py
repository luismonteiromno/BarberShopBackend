from django.db import models


class AbousUs(models.Model):
    name = models.CharField('Nome', max_length=100, default='')
    developed_by = models.CharField('Desenvolvido por:', max_length=150)
    description = models.TextField('Descrição', max_length=255)
    email = models.EmailField('Email para contato:', unique=True)
    phone = models.CharField('Telefone para contato:', max_length=50)

    def __str__(self):
        return f"{self.name} - {self.developed_by}"

    class Meta:
        verbose_name = 'Sobre nós'
        verbose_name_plural = 'Sobre nós'
