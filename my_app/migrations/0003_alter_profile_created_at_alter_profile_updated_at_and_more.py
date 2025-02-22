# Generated by Django 5.1.4 on 2025-01-27 18:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("my_app", "0002_feedbackcategory_manuscript_feedback_questions_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="user_type",
            field=models.CharField(
                default="regular", help_text="User Type of the user", max_length=50
            ),
        ),
    ]
