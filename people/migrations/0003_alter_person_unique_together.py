# Generated by Django 4.1.7 on 2023-05-07 21:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("people", "0002_person_email_person_facebook_person_instagram_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(name="person", unique_together=set(),),
    ]
