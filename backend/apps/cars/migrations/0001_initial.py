# Generated by Django 4.1.13 on 2024-01-12 19:17

from django.db import migrations, models
import djongo.models.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('manufacturer', models.CharField(max_length=100)),
                ('model', models.CharField(max_length=100)),
                ('launch_year', models.PositiveIntegerField()),
                ('engine_config', djongo.models.fields.JSONField()),
                ('features', djongo.models.fields.JSONField(default=list)),
                ('colors', djongo.models.fields.JSONField(default=list)),
                ('categories', djongo.models.fields.JSONField(default=list)),
                ('starting_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
    ]
