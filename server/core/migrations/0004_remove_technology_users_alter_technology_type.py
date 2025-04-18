# Generated by Django 5.1.6 on 2025-04-16 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_technology_users'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='technology',
            name='users',
        ),
        migrations.AlterField(
            model_name='technology',
            name='type',
            field=models.CharField(choices=[('programming', 'Программирование'), ('design', 'Дизайн')], max_length=50, verbose_name='Раздел'),
        ),
    ]
