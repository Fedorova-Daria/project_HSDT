# Generated by Django 5.1.6 on 2025-04-17 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('open', 'Опубликован'), ('under_review', 'На согласовании')], default='draft', max_length=20)),
                ('visible', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('review', 'На рассмотрении'), ('open', 'В поиске'), ('in_progress', 'В работе'), ('done', 'Сделан')], default='draft', max_length=20)),
                ('visible', models.BooleanField(default=False)),
                ('votes_to_approve', models.PositiveIntegerField(default=3)),
                ('approved', models.BooleanField(default=False)),
                ('duration', models.CharField(choices=[('semester', '1 семестр'), ('year', '1 год')], default='semester', max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='TeamResponse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
