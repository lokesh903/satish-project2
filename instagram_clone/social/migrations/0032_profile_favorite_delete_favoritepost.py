# Generated by Django 5.0.7 on 2024-08-05 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0031_remove_profile_favorite_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='favorite',
            field=models.ManyToManyField(null=True, to='social.post'),
        ),
        migrations.DeleteModel(
            name='Favoritepost',
        ),
    ]
