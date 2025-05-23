# Generated by Django 5.2.1 on 2025-05-19 21:19

import articles.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0012_article_ishome_alter_article_isactive'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='date',
        ),
        migrations.RemoveField(
            model_name='article',
            name='imageUrl',
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.CharField(help_text='Yazar(lar) adını girin. Birden fazla yazar varsa virgül ile ayırabilirsiniz.', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='article',
            name='file',
            field=models.FileField(null=True, upload_to='articles/files/', validators=[articles.models.validate_pdf]),
        ),
        migrations.AddField(
            model_name='article',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='slug',
            field=models.SlugField(unique=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='title',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
