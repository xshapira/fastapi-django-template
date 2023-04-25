from django.db import models


class User(models.Model):
    """User model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    posts = models.ManyToManyField(
        "posts.BlogPost",
        blank=True,
        related_name="authors",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
