from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def news_detail(request):
    return render(request, 'news-detail.html')  