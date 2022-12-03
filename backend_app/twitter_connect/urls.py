from django.urls import path, re_path

from . import views

urlpatterns = [
    re_path(r'^get_news_articles/$', views.get_news_articles, name='get_news_articles'),
]