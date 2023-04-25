from django.db import models


class BlogPost(models.Model):
    """Blog post model."""

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    authors = models.ManyToManyField(
        "users.User", on_delete=models.CASCADE, related_name="posts"
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blog post"
        verbose_name_plural = "Blog posts"
