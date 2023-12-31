# Generated by Django 4.2.6 on 2023-11-09 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0028_notes_on_top'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonstatus',
            name='status',
            field=models.CharField(choices=[('not_started', 'Не начато'), ('in_progress', 'В процессе'), ('to_repeat', 'Повторить'), ('next', 'Следущее'), ('done', 'Закончено')], default='not_started', max_length=20),
        ),
    ]
