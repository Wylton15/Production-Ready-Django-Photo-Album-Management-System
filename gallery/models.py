from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


class Album(models.Model):
    """A collection of photos grouped under a named album."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    cover_image = CloudinaryField('cover_image', blank=True, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='albums'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def photo_count(self):
        return self.photos.count()


class RecipePhoto(models.Model):
    """A single photo entry, optionally linked to an Album."""
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    # image = models.ImageField(upload_to='recipes/')
    image = CloudinaryField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='photos'
    )
    album = models.ForeignKey(
        Album, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='photos'
    )

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title