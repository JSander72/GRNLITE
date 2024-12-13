# Generated by Django 5.1.4 on 2024-12-13 05:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_app", "0003_auto_20241213_0450"),
    ]

    operations = [
        migrations.CreateModel(
            name="ManuscriptKeywords",
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
                (
                    "keyword",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="my_app.keyword"
                    ),
                ),
                (
                    "manuscript",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="my_app.manuscript",
                    ),
                ),
            ],
        ),
    ]
