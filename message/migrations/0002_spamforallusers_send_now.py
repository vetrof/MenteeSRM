# Generated by Django 4.2.6 on 2023-11-09 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('message', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='spamforallusers',
            name='send_now',
            field=models.BooleanField(default=False),
        ),
    ]
