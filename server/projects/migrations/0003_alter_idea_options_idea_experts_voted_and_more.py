# Generated by Django 5.1.6 on 2025-03-21 07:14

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_rename_group_universitygroup'),
        ('projects', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='idea',
            options={'verbose_name': 'Идея', 'verbose_name_plural': 'Идеи'},
        ),
        migrations.AddField(
            model_name='idea',
            name='experts_voted',
            field=models.ManyToManyField(blank=True, related_name='voted_for', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='idea',
            name='short_description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='idea',
            name='technologies',
            field=models.ManyToManyField(blank=True, related_name='ideas', to='core.technology'),
        ),
    ]
