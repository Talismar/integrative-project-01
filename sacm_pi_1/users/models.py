from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Default custom user model for SACM-PI-1.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    GENDER_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino')
    ]

    name = models.CharField(max_length=255, blank=False)
    phone_number = models.CharField("Número de telefone", max_length=20, unique=True)

    "Matriculation"
    username = models.CharField(verbose_name='Matriculation', max_length=120, unique=True, blank=False,
                error_messages={
                 "unique": "Usuário com está matricula já existe",
                },)

    first_name = None
    last_name = None

    "111.111.111-11"
    cpf = models.CharField('CPF', max_length=14, unique=True)
    birth_date = models.DateField(verbose_name='Data de nascimento')
    gender = models.CharField('Sexo', max_length=24, choices=GENDER_CHOICES)
    photo = models.ImageField(upload_to='users/photos', blank=True, null=True)

    REQUIRED_FIELDS = ['birth_date', 'email']

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
