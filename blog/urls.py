# blog/urls.py
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='home'),
    path('blog/', views.ArticleListView.as_view(), name='article_list'),
    path('blog/search/', views.SearchResultView.as_view(), name='search'),
    path('blog/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('blog/category/<slug:category_slug>/', views.CategoryListView.as_view(), name='category'),
    path('blog/tag/<slug:tag_slug>/', views.TagListView.as_view(), name='tag'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    
    # Detail views
#     path('blog/<slug:slug>/comment/', views.CommentCreateView.as_view(), name='add_comment'),
    
    # Author and archive views
    # path('authors/', views.AuthorListView.as_view(), name='author_list'),
]