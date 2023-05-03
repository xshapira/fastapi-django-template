# Generated by Django 4.2 on 2023-04-26 10:49

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("posts", "0001_initial"),
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpost",
            name="authors",
            field=models.ManyToManyField(related_name="blog_posts", to="users.user"),
        ),
    ]