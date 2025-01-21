# Generated by Django 5.1.4 on 2025-01-20 19:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("my_app", "0002_remove_betareader_genres_remove_betareader_user_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="betareader",
            name="profile",
            field=models.OneToOneField(
                help_text="The profile associated with this beta reader",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="beta_reader_profile",
                to="my_app.profile",
            ),
        ),
    ]
