from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser

class RolesChoices(models.TextChoices):

    ADMIN = "Admin",'Admin'

    USER = "user","user"

class profile(AbstractUser):

    role = models.CharField(max_length=20,choices = RolesChoices.choices)

    class Meta :

        db_table = 'auth_user'

        verbose_name = 'Profiles'

        verbose_name_plural = 'profiles'

    def __str__(self):
        return self.username