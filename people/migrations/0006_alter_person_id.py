# Generated by Django 4.1.7 on 2023-05-07 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0005_alter_person_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="person",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
