from django.http import HttpResponse
from django.shortcuts import render

def index(request):
    return render(request, 'pages/index.html')
def about(request):
    return render(request, 'pages/about.html')

def contact(request):
    return render(request, 'pages/contact.html')

