# Generated by Django 5.1.4 on 2025-01-03 02:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_app", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="customuser",
            name="profile_picture",
            field=models.ImageField(blank=True, null=True, upload_to="profiles/"),
        ),
    ]