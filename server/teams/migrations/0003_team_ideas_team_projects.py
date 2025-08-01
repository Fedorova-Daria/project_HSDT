# Generated by Django 5.1.6 on 2025-06-23 16:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_idea_team_idea_teams_working_on_alter_idea_status_and_more'),
        ('teams', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='ideas',
            field=models.ManyToManyField(blank=True, related_name='teams_working_on_ideas', to='projects.idea'),
        ),
        migrations.AddField(
            model_name='team',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='teams_working_on', to='projects.project'),
        ),
    ]
