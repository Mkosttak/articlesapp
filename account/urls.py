from django.urls import path
from . import views


urlpatterns = [
    path('login', views.user_login, name='user_login'),
    path('register', views.user_register, name='user_register'),
    path('change-password', views.change_password, name='change_password'),
    path('logout', views.user_logout, name='user_logout'),
    path('profile', views.profile, name='profile'),
    path('my-articles', views.my_articles, name='my_articles'),
    path('authors', views.authors_list, name='authors_list'),
    path('admin-authors',views.admin_authors,name="admin_authors"),
    path('admin/editors/<int:author_id>/edit/', views.authors_edit, name='authors_edit'),
    path('author/<int:author_id>', views.author_detail, name='author_detail'),


]