# Generated by Django 4.2.6 on 2023-12-01 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tbot', '0004_alter_telegramuser_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='TgSpam',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('all_tg_user', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('message', models.TextField()),
            ],
        ),
    ]
