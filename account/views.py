from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from account.forms import LoginUserForm, NewUserForm, UserPasswordChangeForm, AuthorProfileForm, UserProfileForm
from account.models import Author
from articles.models import Article


def user_login(request):
    if request.user.is_authenticated and "next" in request.GET:
        return render(request, 'account/login.html', {"error": "Yetkiniz Yok!"})
    if request.method == "POST":
        form = LoginUserForm(request, data=request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.add_message(request, messages.SUCCESS, 'Başarılı bir şekilde giriş yaptınız!')
                nextUrl = request.GET.get('next', None)
                if nextUrl is None:
                    return redirect('index')
                else:
                    return redirect(nextUrl)
            else:
                return render(request, 'account/login.html', {"form": form})

        else:

            messages.add_message(request, messages.ERROR, 'Username ya da password hatalı!')
            return render(request, 'account/login.html', {"form": form})

    else:
        form = LoginUserForm()
        return render(request, 'account/login.html', {"form": form})


def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Create author profile for the user
            Author.objects.create(user=user)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.add_message(request, messages.SUCCESS,
                                 'Başarılı bir şekilde kayıt oldunuz! Profilinizi düzenleyebilirsiniz.')
            return redirect('profile')
        else:
            return render(request, 'account/register.html', {"form": form})
    else:
        form = NewUserForm()
        return render(request, 'account/register.html', {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Parolanız Güncellendi!')
            return redirect('change_password')
        else:
            messages.error(request, 'Tekrar Deneyiniz!')
            return render(request, 'account/change-password.html', {"form": form})
    form = UserPasswordChangeForm(request.user)
    return render(request, 'account/change-password.html', {"form": form})


def user_logout(request):
    messages.add_message(request, messages.SUCCESS, 'Çıkış Başarılı!')
    logout(request)
    return redirect('index')


@login_required
def profile(request):
    # Get or create author profile
    author, created = Author.objects.get_or_create(user=request.user)

    user_form = UserProfileForm(instance=request.user)
    author_form = AuthorProfileForm(instance=author)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=request.user)
        author_form = AuthorProfileForm(request.POST, request.FILES, instance=author)

        if user_form.is_valid() and author_form.is_valid():
            user_form.save()
            author_form.save()
            messages.success(request, 'Profiliniz başarıyla güncellendi!')
            return redirect('profile')

    context = {
        'user_form': user_form,
        'author_form': author_form,
        'author': author
    }
    return render(request, 'account/profile.html', context)


@login_required
def my_articles(request):
    articles = Article.objects.filter(author=request.user)
    return render(request, 'account/my-articles.html', {'articles': articles})


def authors_list(request):
    authors = Author.objects.filter(is_approved=True)
    return render(request, 'account/authors-list.html', {'authors': authors})


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id, is_approved=True)
    articles = Article.objects.filter(author=author.user, isActive=True)
    return render(request, 'account/author-detail.html', {'author': author, 'articles': articles})

@login_required
def profile_view(request):
    user = request.user
    author, created = Author.objects.get_or_create(user=user)

    if request.method == "POST":
        user_form = UserProfileForm(request.POST, instance=user)
        author_form = AuthorProfileForm(request.POST, request.FILES, instance=author)

        if user_form.is_valid() and author_form.is_valid():
            user_form.save()
            author_form.save()
            messages.success(request, "Profil başarıyla güncellendi.")
            return redirect('profile')
        else:
            messages.error(request, "Lütfen formdaki hataları düzeltin.")
    else:
        user_form = UserProfileForm(instance=user)
        author_form = AuthorProfileForm(instance=author)

    user_articles = Article.objects.filter(author=user)

    context = {
        'user_form': user_form,
        'author_form': author_form,
        'articles': user_articles,
        'author': author,
    }

    return render(request, 'account/profile.html', context)