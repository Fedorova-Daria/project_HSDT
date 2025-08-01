# Generated by Django 5.1.6 on 2025-05-23 07:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='members',
            field=models.ManyToManyField(blank=True, related_name='teams', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='team',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='owned_team', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='teamjoinrequest',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='join_requests', to='teams.team'),
        ),
        migrations.AddField(
            model_name='teamjoinrequest',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_join_requests', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='teamjoinrequest',
            unique_together={('user', 'team')},
        ),
    ]
