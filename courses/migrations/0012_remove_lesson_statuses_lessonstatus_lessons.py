# Generated by Django 4.2.6 on 2023-10-11 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0011_lesson_statuses_alter_lessonstatus_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lesson',
            name='statuses',
        ),
        migrations.AddField(
            model_name='lessonstatus',
            name='lessons',
            field=models.ManyToManyField(related_name='lesson_statuses', to='courses.lesson'),
        ),
    ]
