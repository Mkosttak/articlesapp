from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from datetime import date, datetime
from .forms import ArticleCreateForm, ArticleEditForm, UploadForm
from .models import Article, Category, UploadModel
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

data = {
    "topoloji" : "Topoloji makaleleri",
    "cebir" : "Cebir makaleleri",
    "analiz" : "Analiz makaleleri",
    "deneme" : "Deneme makaleleri"
}

db = {
    "articles": [
        {
            "title": "makale1",
            "description": "makale1 açıklaması",
            "imageUrl": "1.jpg",
            "slug": "makale-1",
            "date": datetime.now(),
            "isActive": True,
            "isUpdate": False
        },
        {
            "title": "makale2",
            "description": "makale2 açıklaması",
            "imageUrl": "2.jpg",
            "slug": "makale-2",
            "date": date(2022,10,10),
            "isActive": False,
            "isUpdate": True
        },
        {
            "title": "makale3",
            "description": "makale3 açıklaması",
            "imageUrl": "3.jpg",
            "slug": "makale-3",
            "date": date(2022,10,10),
            "isActive": True,
            "isUpdate": True
        }
    ],
    "category": [
        {"id": 1,"name":"topoloji", "slug": "topoloji"},
        {"id": 2,"name":"cebir", "slug": "cebir"},
        {"id": 3,"name":"analiz", "slug": "analiz"},
    ]
}

def index(request):
    makaleler = Article.objects.filter(isActive=True, isHome=True)
    kategoriler = Category.objects.all()

    return render(request, 'articles/index.html',{
        'categories': kategoriler,
        'articles': makaleler,

    })


def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        articles = Article.objects.filter(isActive=True, title__contains=q).order_by("date")
        categoris = Category.objects.all()
    else:
        return redirect("/makale")


    return render(request, 'articles/search.html', {
        'categories': categoris,
        'articles': articles,
    })


def isAdmin(user):
    return user.is_superuser


@user_passes_test(isAdmin)
def article_create(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect("/makale")
    else:
        form = ArticleCreateForm()

    return render(request, 'articles/article_create.html', {"form": form})

@login_required()
def article_list(request):
    articles = Article.objects.all().order_by("date")
    categoris = Category.objects.all()

    return render(request, 'articles/article-list.html', {
        'categories': categoris,
        'articles': articles,
    })

def article_edit(request,id):
    article = get_object_or_404(Article, pk=id)
    if request.method == "POST":
        form = ArticleEditForm(request.POST, request.FILES,instance=article)
        form.save()
        return redirect('article_list')

    else:
        form = ArticleEditForm(instance=article)
    return render(request, 'articles/article-edit.html', {"form": form})


def article_delete(request,id):
    article = get_object_or_404(Article, pk=id)
    if request.method == "POST":
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/article-delete.html', {
        'article': article,
    })

def upload(request):
    if request.method == "POST":
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            model = UploadModel(image=request.FILES["image"])
            model.save()
            return render(request, 'articles/success.html')
    else:
        form = UploadForm()
    return render(request, 'articles/upload.html',{"form": form})


def details(request,slug):
    """try:
        article = Article.objects.get(id=kurs_id)
    except:
        raise Http404("Kurs bulunamadı")"""

    article = get_object_or_404(Article, slug=slug)
    context = {
        'article': article
    }
    return render(request, 'articles/details.html', context)


def getArticlesByCategory(request,slug):
    articles = Article.objects.filter(categories__slug=slug,isActive=True)
    categoris = Category.objects.all()

    paginator = Paginator(articles, 2)
    page = request.GET.get('page',1)
    page_obj = paginator.page(page)

    return render(request, 'articles/list.html',{
        'categories': categoris,
        'page_obj': page_obj,
        'seciliKategori': slug,
    })

