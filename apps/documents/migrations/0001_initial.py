# Generated by Django 5.0.6 on 2024-07-27 20:52

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

from ..utils.migration_handlers import insert_initial_data


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TopicModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('topic_name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'topic',
                'verbose_name_plural': 'topics',
            },
        ),
        migrations.CreateModel(
            name='DocumentModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('document_name', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('weight', models.PositiveSmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('for_workshop', models.BooleanField(default=True)),
                ('for_simulation', models.BooleanField(default=True)),
                ('topic_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='documents.topicmodel')),
            ],
            options={
                'verbose_name': 'document',
                'verbose_name_plural': 'documents',
            },
        ),
        migrations.RunPython(insert_initial_data),
    ]
