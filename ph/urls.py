from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListAV.as_view(), name = "article-index-page"),
    path("<str:pk>/", views.ArticleDetailAV.as_view(), name = "article-detail-page")
]