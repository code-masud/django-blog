from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('archive/<int:year>/<int:month>/', views.ArticleMonthArchiveView.as_view(month_format='%m'),name='archive'),
    path('post/add/', views.ArticleAddView.as_view(), name='article_add'),
    path('post/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('post/<slug:slug>/edit/', views.ArticleEditView.as_view(), name='article_edit'),
    path('post/<slug:slug>/delete/', views.ArticleDeleteView.as_view(), name='article_delete'),
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag'),
    path('post/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
]