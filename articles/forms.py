from django import forms
from .models import Article

class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'description', 'file', 'categories']
        labels = {
            'title': 'Başlık',
            'description': 'Açıklama',
            'file': 'PDF Dosyası',
            'categories': 'Kategoriler',
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title', 'description', 'file', 'categories',
            'isActive', 'isHome', 'admin_note'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'file': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'admin_note': forms.Textarea(attrs={'class': 'form-control'}),
        }
