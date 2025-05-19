
from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('search',views.search, name='search'),
    path('article-create', views.article_create, name='article_create'),
    path('article-list', views.article_list, name='article_list'),
    path('article-edit/<int:id>',views.article_edit, name='article_edit'),
    path('article-delete/<int:id>',views.article_delete, name='article_delete'),
    path('upload' ,views.upload, name='uploadimage'),
    path('<slug:slug>', views.details, name='article_details'),
    path('kategori/<slug:slug>' , views.getArticlesByCategory, name='articles_by_category')

]