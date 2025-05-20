from django.utils.text import slugify
from django.db import models
from django.contrib.auth.models import User
import os
from django.core.exceptions import ValidationError

def validate_pdf(value):
    ext = os.path.splitext(value.name)[1]
    if ext.lower() != '.pdf':
        raise ValidationError('Yalnızca PDF dosyalarına izin verilir.')


import uuid

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=False, default="", unique=True, db_index=True)

    def __str__(self):
        return self.name


def article_file_upload_to(instance, filename):
    ext = filename.split('.')[-1]
    base_slug = slugify(instance.title)
    filename = f"{base_slug}.{ext}"
    return f'uploads/articles/files/{filename}'

class Article(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to=article_file_upload_to, null=True, blank=True)
    date = models.DateField(auto_now=True)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default=False)
    slug = models.SlugField(null=False, blank=True, unique=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    admin_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            num = 1
            while Article.objects.filter(slug=unique_slug).exclude(pk=self.pk).exists():
                unique_slug = f"{base_slug}-{num}"
                num += 1
            self.slug = unique_slug
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-updated_at']

