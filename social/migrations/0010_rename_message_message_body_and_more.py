# Generated by Django 5.0.7 on 2024-08-20 09:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0009_remove_profile_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='message',
            old_name='message',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='status',
            new_name='is_read',
        ),
    ]
