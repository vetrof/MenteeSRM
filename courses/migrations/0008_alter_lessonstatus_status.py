# Generated by Django 4.2.6 on 2023-10-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_lessonstatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonstatus',
            name='status',
            field=models.CharField(choices=[('not_started', 'не начато'), ('in_progress', 'В процессе'), ('done', 'Закончено')], default='not_started', max_length=20),
        ),
    ]
