# Generated by Django 4.1.7 on 2023-05-10 16:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("society", "0006_society_recruitment_form_alter_society_logo_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="society",
            name="page_color",
            field=models.CharField(default="00629A", max_length=8),
        ),
        migrations.AlterField(
            model_name="society",
            name="subgroup_label",
            field=models.CharField(
                choices=[("Subgroups", "Subgroups"), ("Projects", "Projects")],
                default=("Subgroups", "Subgroups"),
                max_length=30,
            ),
        ),
    ]