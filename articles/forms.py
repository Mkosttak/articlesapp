from django import forms

from articles.models import Article


# class ArticleCreateForm(forms.Form):
#     title = forms.CharField(label="Makale Başlık",
#                             required=False,
#                             error_messages={"required": "Lütfen Başlık Giriniz."},
#                             widget=forms.TextInput(attrs={"class": "form-control"}))
#     description = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control"}))
#     imageUrl = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control"}))
#     slug = forms.SlugField(widget=forms.TextInput(attrs={"class": "form-control"}))


class ArticleCreateForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','description','image','slug']
        labels = {
            'title': 'Makale Başlık',
            'description': 'Açıklama',
            'imageUrl': 'Resim',
            'slug': 'Slug',
        }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'slug': forms.TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            'title': {
                'required': 'Lütfen Başlık Giriniz.'
            }
        }

class ArticleEditForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title','description','image','slug']
        labels = {
            'title': 'Makale Başlık',
            'description': 'Açıklama',
            'imageUrl': 'Resim',
            'slug': 'Slug',
        }
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'description': forms.Textarea(attrs={"class": "form-control"}),
            'slug': forms.TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            'title': {
                'required': 'Lütfen Başlık Giriniz.'
            }
        }

class UploadForm(forms.Form):
    image = forms.ImageField()
