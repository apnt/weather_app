# Generated by Django 5.0.7 on 2024-08-04 16:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Measurement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("uuid", models.UUIDField(default=uuid.uuid4, unique=True)),
                ("date_captured", models.DateTimeField()),
                ("date_registered", models.DateTimeField(auto_now_add=True)),
                ("temperature", models.DecimalField(decimal_places=2, max_digits=5)),
                ("humidity", models.DecimalField(decimal_places=2, max_digits=5)),
                ("precipitation", models.DecimalField(decimal_places=1, max_digits=5)),
                ("wind_direction", models.DecimalField(decimal_places=2, max_digits=5)),
                ("wind_speed", models.DecimalField(decimal_places=2, max_digits=5)),
            ],
            options={
                "ordering": ("date_captured",),
            },
        ),
    ]