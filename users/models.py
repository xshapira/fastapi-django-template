from django.db import models


class User(models.Model):
    """User model."""

    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    posts = models.ForeignKey(
        "posts.BlogPost",
        blank=True,
        null=True,
        on_delete=models.CASCADE,
        related_name="blog_users",
    )

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
