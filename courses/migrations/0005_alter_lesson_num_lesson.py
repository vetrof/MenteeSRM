# Generated by Django 4.2.6 on 2023-10-10 19:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0004_topic_num_topic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='num_lesson',
            field=models.FloatField(),
        ),
    ]
