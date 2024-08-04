# Generated by Django 5.0.7 on 2024-08-04 16:03

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Station",
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
                ("name", models.CharField(max_length=50, unique=True)),
                ("latitude", models.DecimalField(decimal_places=6, max_digits=8)),
                ("longitude", models.DecimalField(decimal_places=6, max_digits=9)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ("name",),
            },
        ),
    ]
