from django.contrib import admin
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isActive', 'created_at')
    list_filter = ('isActive',)
    list_editable = ('isActive',)
    fields = (
        'title', 'description', 'file', 'categories', 'author',
        'isActive', 'isHome', 'admin_note', 'slug'
    )
    filter_horizontal = ('categories',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'article_count')
    prepopulated_fields = {'slug': ('name',)}

    def article_count(self, obj):
        return obj.article_set.count()
