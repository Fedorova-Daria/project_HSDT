# Generated by Django 5.1.6 on 2025-05-27 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_semester'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='semester',
            options={'ordering': ['-year', 'semester'], 'verbose_name': 'Семестр', 'verbose_name_plural': 'Семестры'},
        ),
    ]
