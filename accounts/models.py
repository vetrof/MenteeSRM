from django.db import models
from django.conf import settings


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    telegram_user = models.CharField(max_length=100, blank=True, null=True)
    telegram_chatid = models.IntegerField(blank=True, null=True)
    mentee = models.BooleanField(default=False)
    current_mentee = models.BooleanField(default=False)
    g1 = models.BooleanField(default=False)
    g2 = models.BooleanField(default=False)
    g3 = models.BooleanField(default=False)

    def __str__(self):
        return f'Profile of {self.user.username}'
