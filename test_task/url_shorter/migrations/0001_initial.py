# Generated by Django 3.2.4 on 2021-06-15 15:39

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="ShortenedLink",
            fields=[
                ("original_link", models.TextField()),
                (
                    "subpart",
                    models.CharField(max_length=5, primary_key=True, serialize=False),
                ),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                ("session_id", models.TextField()),
            ],
        ),
    ]
