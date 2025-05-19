from django.contrib import admin
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','isActive','isHome', "slug", "category_list")
    list_display_links = ('title','slug',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ["title","isActive","isHome"]
    list_editable = ("isActive","isHome")
    search_fields = ("title","description")

    def category_list(self,obj):
        return ", ".join([c.name for c in obj.categories.all().order_by("name")])
    category_list.short_description = "Kategoriler"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','slug', "article_count")
    prepopulated_fields = {'slug': ('name',)}


    def article_count(self,obj):
        return obj.article_set.count()