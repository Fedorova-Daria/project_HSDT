# Generated by Django 5.1.6 on 2025-03-21 07:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_group_alter_technology_options'),
        ('users', '0008_rename_group_account_university_group_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Group',
            new_name='UniversityGroup',
        ),
    ]
