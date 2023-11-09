from django.db import models


class SpamForAllUsers(models.Model):
    subject = models.CharField(max_length=200)
    message = models.TextField()
    only_admin = models.BooleanField(default=False)
    send_now = models.BooleanField(default=False)


