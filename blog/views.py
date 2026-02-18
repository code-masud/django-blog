from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Article, Category, Tag, Comment
from .forms import CommentForm

class ArticleListView(generic.ListView):
    model = Article
    template_name = 'blog/article_list.html'
    paginate_by = 6
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Blog | Home'
        return context

class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    
    def get_queryset(self):
        return Article.objects.filter(status=Article.Status.PUBLISHED, published_at__isnull=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titile'] = 'f{self.object.title} | Detail' 
        return context

class AuthorDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/author_detail.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titile'] = 'f{self.object.title} | Author' 
        return context

class CategoryListView(generic.ListView):
    model = Category
    template_name = 'blog/category_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Blog | Category'
        return context

class TagListView(generic.ListView):
    model = Tag
    template_name = 'blog/tag_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Blog | Tag'
        return context

class SearchResultView(generic.ListView):
    model = Article
    template_name = 'blog/search_result_list.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'My Blog | Search Result'
        return context