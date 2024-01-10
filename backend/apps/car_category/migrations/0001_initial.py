# Generated by Django 4.1.13 on 2024-01-10 18:33

from django.db import migrations, models
import djongo.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CarCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=255, unique=True)),
                ('baseline_parameters', djongo.models.fields.JSONField()),
                ('description', models.TextField()),
            ],
        ),
    ]
