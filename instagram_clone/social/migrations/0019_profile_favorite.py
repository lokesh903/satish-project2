# Generated by Django 5.0.7 on 2024-07-28 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0018_alter_post_timestamps'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite',
            field=models.ManyToManyField(to='social.post'),
        ),
    ]
