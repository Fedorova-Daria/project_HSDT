# Generated by Django 5.1.6 on 2025-05-27 12:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_remove_project_duration_semester_project_semester'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='experts_voted',
        ),
    ]
