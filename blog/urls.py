from django.contrib import admin
from django.urls import path

from . import views

app_name = "blog"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("category/<cat>/", views.CategoryView.as_view(), name="category"),
    path("search/", views.SearchView.as_view(), name="search"),
    path("article/<str:category>/<slug:slug>/", views.articleView, name="article"),
    path("show-content/", views.showContent, name="content"),
    path("cat-show-content/", views.catShowContent, name="catcontent"),
    path("fake-news/", views.fake_news, name="fake-news"),
    path('predict/', views.predict, name='predict')
]
