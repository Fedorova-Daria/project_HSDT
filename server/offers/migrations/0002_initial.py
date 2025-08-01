# Generated by Django 5.1.6 on 2025-05-23 07:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('offers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='offers',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_offers', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='offers',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer', to=settings.AUTH_USER_MODEL),
        ),
    ]
