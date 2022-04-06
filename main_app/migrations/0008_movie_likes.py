# Generated by Django 4.0.3 on 2022-04-06 04:04

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0007_remove_movie_reviews_review_movie'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='likes',
            field=models.ManyToManyField(related_name='movie_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
