from datetime import date
from django.views import generic
from django.db.models import Q
from .models import Article, Category, Tag, Comment
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from .forms import CommentForm, ArticleForm
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone

class ArticleListView(generic.ListView):
    model = Article
    template_name = 'blog/article_list.html'
    paginate_by = 5

    def get_queryset(self):
        return Article.alive_objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Home'
        return context

class ArticleDetailView(generic.DetailView):
    model = Article
    template_name = 'blog/article_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

    def get_queryset(self):
        return Article.alive_objects.filter(status=Article.Status.PUBLISHED, published_at__isnull=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['form'] = CommentForm()
        return context
    
class ArticleEditView(generic.UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:home')

    def get_queryset(self):
        return Article.alive_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Edit: {self.object.title}'
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        messages.success(self.request, f'Article "{self.object.title}" updated successfully.')
        return super().form_valid(form)

class ArticleDeleteView(generic.DeleteView):
    model = Article
    success_url = reverse_lazy('blog:home')
    template_name = 'blog/article_confirm_delete.html'

    def get_queryset(self):
        return Article.alive_objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = f'Delete: {self.object.title}'
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_deleted = True
        self.object.deleted_by = request.user
        self.object.deleted_at = timezone.now()
        self.object.save()
        messages.success(request, 'Article deleted successfully.')
        return super().delete(request, *args, **kwargs)


class ArticleAddView(generic.CreateView):
    model = Article
    form_class = ArticleForm
    template_name = 'blog/article_form.html'
    success_url = reverse_lazy('blog:home')

    def get_queryset(self):
        return Article.alive_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = 'Add Article'
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.author = self.request.user
        if form.instance.status == Article.Status.PUBLISHED:
            form.instance.published_at = timezone.now()
        messages.success(self.request, 'Article created successfully.')
        return super().form_valid(form)
    
    
class CategoryDetailView(generic.DetailView):
    model = Category
    template_name = 'blog/category_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 5

    def get_queryset(self):
        return Article.alive_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        article_list = self.object.articles.filter(published_at__isnull=False)

        paginator = Paginator(article_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['article_list'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['paginator'] = paginator
        return context
    
class TagDetailView(generic.DetailView):
    model = Tag
    template_name = 'blog/tag_detail.html'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    paginate_by = 5

    def get_queryset(self):
        return Article.alive_objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'#{self.object.name}'
        article_list = self.object.articles.filter(published_at__isnull=False)

        paginator = Paginator(article_list, self.paginate_by)
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context['article_list'] = page_obj
        context['page_obj'] = page_obj
        context['is_paginated'] = page_obj.has_other_pages()
        context['paginator'] = paginator
        return context

class SearchView(generic.ListView):
    model = Article
    template_name = 'blog/search_results.html'
    context_object_name = 'article_list'
    paginate_by = 5

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.alive_objects.filter(
                Q(title__icontains=query) |
                Q(slug__icontains=query) |
                Q(author__username__icontains=query) |
                Q(content__icontains=query),
                status=Article.Status.PUBLISHED
            )
        return Article.alive_objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['title'] = f'Search result for "{context['query']}"'
        return context
    
class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/article_detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.article = get_object_or_404(Article, slug=self.kwargs['slug'])
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse_lazy('blog:article_detail',
            kwargs={
                'slug': self.article.slug,
            }
        )
    
    def form_valid(self, form):
        form.instance.article = self.article
        form.instance.user = self.request.user
        form.instance.created_by = self.request.user
        form.instance.is_approved = True
        messages.success(self.request, 'Thank you for your comment!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.article.title
        context['article'] = self.article
        context['form'] = CommentForm()
        return context 

class ArticleMonthArchiveView(generic.MonthArchiveView):
    queryset = Article.alive_objects.filter(status=Article.Status.ARCHIVE)
    date_field = 'published_at'
    allow_future = False
    template_name = 'blog/post_archive_month.html'
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['year'] = self.kwargs['year']
        context['month'] = self.kwargs['month']
        context['date'] = date(year=self.kwargs['year'], month=self.kwargs['month'], day=1)
        context['title'] = f'{self.kwargs['month']} {self.kwargs['year']}'
        return context
