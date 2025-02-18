# Generated by Django 5.1.6 on 2025-02-18 17:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_project_owner_alter_idea_initiator_and_more'),
        ('users', '0004_rename_date_joined_account_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='idea',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_ideas', to='users.account'),
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='projects_initiated', to='projects.team'),
        ),
    ]
