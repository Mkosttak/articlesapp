from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from .forms import ArticleCreateForm, ArticleEditForm, UserArticleEditForm
from .models import Article, Category
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Q
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages

# Giriş sayfası (ana sayfa)
def index(request):
    query = request.GET.get("q", "").strip()
    if query != "":
        makaleler = Article.objects.filter(
            Q(isActive=True, isHome=True),
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        )
    else:
        makaleler = Article.objects.filter(isActive=True, isHome=True)

    kategoriler = Category.objects.all()
    return render(request, 'articles/index.html', {
        'categories': kategoriler,
        'articles': makaleler,
        'query': query
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
            article.isActive = False
            article.save()
            form.save_m2m()
            return redirect('account:my_articles')
        else:
            return render(request, 'articles/article-create.html', {
                "form": form,
                "error": True,
                "msg": "Lütfen yalnızca PDF formatında dosya yükleyin."
            })
    else:
        form = ArticleCreateForm()
    return render(request, 'articles/article-create.html', {"form": form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def article_list(request):
    query = request.GET.get("q", "").strip()
    if query != "":
        articles = Article.objects.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(author__first_name__icontains=query) |
            Q(author__last_name__icontains=query)
        ).select_related('author').order_by("-updated_at")
    else:
        articles = Article.objects.all().select_related('author').order_by("-updated_at")

    return render(request, 'articles/article-list.html', {
        'articles': articles,
        'query': query
    })

@login_required
def article_edit(request, id):
    try:
        article = get_object_or_404(Article, pk=id)
    except ValueError:
        article = get_object_or_404(Article, slug=id)

    if request.user.is_superuser:
        # Admin düzenliyor
        form_class = ArticleEditForm
        template = 'articles/article-edit-admin.html'
    elif request.user == article.author:
        # Normal kullanıcı kendi makalesini düzenliyor
        form_class = UserArticleEditForm
        template = 'articles/article-edit.html'
    else:
        raise PermissionDenied()

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=article)
        if form.is_valid():
            updated_article = form.save(commit=False)
            if not request.user.is_superuser:
                updated_article.isActive = False
                updated_article.isHome = False
            updated_article.save()
            form.save_m2m()
            return redirect('account:my_articles' if not request.user.is_superuser else 'article_list')
    else:
        form = form_class(instance=article)

    return render(request, template, {"form": form})

@login_required
@csrf_protect
def article_delete(request, id):
    try:
        article = get_object_or_404(Article, pk=id)
    except ValueError:
        article = get_object_or_404(Article, slug=id)

    if not request.user.is_superuser and article.author != request.user:
        return redirect('index')

    if request.method == "POST":
        article.delete()
        messages.success(request, "Makale başarıyla silindi.")
        if request.user.is_superuser:
            return redirect('article_list')
        else:
            return redirect('account:my_articles')

    return render(request, 'articles/article-delete.html', {'article': article})

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

@login_required
def profile_edit(request):
    # ProfileEditForm ve Profile importlarını kaldırıyorum, çünkü artık bu form ve model burada kullanılmıyor.
    pass