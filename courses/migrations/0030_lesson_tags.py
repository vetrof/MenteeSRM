# Generated by Django 4.2.6 on 2023-11-09 12:48

from django.db import migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx'),
        ('courses', '0029_alter_lessonstatus_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='tags',
            field=taggit.managers.TaggableManager(help_text='A comma-separated list of tags.', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
