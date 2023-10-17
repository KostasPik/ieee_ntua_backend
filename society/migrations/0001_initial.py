# Generated by Django 4.1.7 on 2023-04-29 14:20

import backend.storages
import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion
import society.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Society",
            fields=[
                (
                    "title",
                    models.CharField(
                        help_text="Δεν αλλάζει ο τίτλος που θα βάλετε. Εάν θέλετε να τον αλλάξετε φτιάξτε καινούργιο society και διαγράψτε αυτό.",
                        max_length=200,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("short_title", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=200, unique=True)),
                (
                    "logo",
                    models.ImageField(
                        storage=backend.storages.OverwriteStorage,
                        upload_to=society.models.Society.get_image_path,
                    ),
                ),
                (
                    "hero_image",
                    models.ImageField(
                        storage=backend.storages.OverwriteStorage,
                        upload_to=society.models.Society.get_background_hero_image,
                    ),
                ),
                ("greek_body", ckeditor.fields.RichTextField(max_length=10000)),
                ("english_body", ckeditor.fields.RichTextField(max_length=10000)),
                (
                    "subgroup_label",
                    models.CharField(
                        choices=[("Subgroups", "Subgroups"), ("Projects", "Projects")],
                        max_length=30,
                    ),
                ),
                ("page_color", models.CharField(default="00629A", max_length=6)),
            ],
            options={"verbose_name_plural": "Societies",},
        ),
        migrations.CreateModel(
            name="SubGroup",
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
                ("title", models.CharField(max_length=150)),
                (
                    "thumbnail",
                    models.ImageField(
                        max_length=350, upload_to=society.models.SubGroup.get_image_path
                    ),
                ),
                (
                    "greek_body",
                    models.TextField(
                        help_text="350 characters maximum.", max_length=350
                    ),
                ),
                (
                    "english_body",
                    models.TextField(
                        help_text="350 characters maximum.", max_length=350
                    ),
                ),
                (
                    "society",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="society.society",
                    ),
                ),
            ],
            options={"verbose_name_plural": "SubGroups",},
        ),
        migrations.AddIndex(
            model_name="society",
            index=models.Index(fields=["slug"], name="society_soc_slug_68243a_idx"),
        ),
        migrations.AlterUniqueTogether(
            name="subgroup", unique_together={("title", "society")},
        ),
    ]
