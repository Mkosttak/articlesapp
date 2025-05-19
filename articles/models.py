from django.db import models
from django.utils.text import slugify
import itertools
from ckeditor.fields import RichTextField

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(null=False,default="",unique=True, db_index=True)

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=50)
    description = RichTextField()
    image = models.ImageField(upload_to="images",default="")
    date = models.DateField(auto_now=True)
    isActive = models.BooleanField(default=False)
    isHome = models.BooleanField(default=False)
    slug = models.SlugField(null=False,default="",blank=True,unique=True, db_index=True)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title

class UploadModel(models.Model):
    image = models.ImageField(upload_to="images")