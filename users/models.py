from django.db import models
from django.contrib.auth.models import AbstractUser
from barber_shop.models import Company

# Create your models here.
TYPE_USER = (
    ('cliente', 'Cliente'),
    ('barbeiro', 'Barbeiro')
)


class UserProfile(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    username = models.CharField('Nome', max_length=40, null=True, blank=True)
    type = models.CharField('Tipo do usuário', choices=TYPE_USER, max_length=50, default='')
    owner_company = models.ForeignKey(Company, related_name="distributor_user", verbose_name="Gerente de", on_delete=models.SET_NULL, blank=True, null=True)
    owner = models.BooleanField('Dono de alguma barbearia?', default=False)
    full_name = models.CharField("Nome Completo", max_length=512, blank=True, null=True)
    email = models.EmailField('E-mail', unique=True)
    image = models.ImageField('Foto de perfil', blank=True, null=True)
    description = models.TextField('Descrição de usuário', max_length=500, default='', blank=True, null=True)
    token_google = models.TextField('Token', default='', max_length=500)
    

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="user_profiles",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="user_profiles",
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

    def __str__(self):
        return self.username  
