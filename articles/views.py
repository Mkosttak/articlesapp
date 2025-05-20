from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleCreateForm, ArticleEditForm
from .models import Article, Category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test

# Giriş sayfası (ana sayfa)
def index(request):
    makaleler = Article.objects.filter(isActive=True, isHome=True)
    kategoriler = Category.objects.all()
    return render(request, 'articles/index.html', {
        'categories': kategoriler,
        'articles': makaleler,
    })

# Arama fonksiyonu
def search(request):
    if "q" in request.GET and request.GET["q"] != "":
        q = request.GET["q"]
        articles = Article.objects.filter(isActive=True, title__icontains=q).order_by("date")
        categories = Category.objects.all()
    else:
        return redirect("/makale")

    return render(request, 'articles/search.html', {
        'categories': categories,
        'articles': articles,
    })

# Sadece admin girebilir
def isAdmin(user):
    return user.is_superuser

@login_required()
def article_create(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.isActive = False  # Yayında değil, admin onayı bekliyor
            article.save()
            form.save_m2m()
            return redirect('my_articles')  # ya da başka uygun sayfa
    else:
        form = ArticleCreateForm()

    return render(request, 'articles/article-create.html', {"form": form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def article_list(request):
    articles = Article.objects.all().order_by("-updated_at")
    return render(request, 'articles/article-list.html', {
        'articles': articles
    })

@login_required
@user_passes_test(lambda u: u.is_superuser)
def article_edit(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == "POST":
        form = ArticleEditForm(request.POST, request.FILES, instance=article)
        if form.is_valid():
            form.save()
            return redirect('article_list')
    else:
        form = ArticleEditForm(instance=article)
    return render(request, 'articles/article-edit.html', {"form": form})

# Makale silme
def article_delete(request, id):
    article = get_object_or_404(Article, pk=id)
    if request.method == "POST":
        article.delete()
        return redirect('article_list')
    return render(request, 'articles/article-delete.html', {
        'article': article,
    })

# Dosya yükleme (örnek amaçlı)
def upload(request):
    pass
    # if request.method == "POST":
    #     form = UploadForm(request.POST, request.FILES)
    #     if form.is_valid():
    #         model = UploadModel(image=request.FILES["image"])
    #         model.save()
    #         return render(request, 'articles/success.html')
    # else:
    #     form = UploadForm()
    # return render(request, 'articles/upload.html', {"form": form})

# Makale detay sayfası
def details(request, slug):
    article = get_object_or_404(Article, slug=slug)
    context = {
        'article': article
    }
    return render(request, 'articles/details.html', context)

# Kategoriye göre filtrelenmiş makaleler
def getArticlesByCategory(request, slug):
    articles = Article.objects.filter(categories__slug=slug, isActive=True)
    categories = Category.objects.all()

    paginator = Paginator(articles, 2)
    page = request.GET.get('page', 1)
    page_obj = paginator.page(page)

    return render(request, 'articles/list.html', {
        'categories': categories,
        'page_obj': page_obj,
        'seciliKategori': slug,
    })
