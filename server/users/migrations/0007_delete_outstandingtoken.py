# Generated by Django 5.1.6 on 2025-03-05 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_outstandingtoken'),
    ]

    operations = [
        migrations.DeleteModel(
            name='OutstandingToken',
        ),
    ]
