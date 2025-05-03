from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('news-detail/', views.news_detail, name='news-detail'),  # Optional
]