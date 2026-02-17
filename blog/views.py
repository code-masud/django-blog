# blog/views.py
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Article, Category, Tag, Comment
from .forms import CommentForm

class ArticleListView(generic.ListView):
    """Homepage with paginated blog posts"""
    model = Article
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    # def get_queryset(self):
    #     """Return published posts, optionally filtered by category/tag"""
    #     queryset = Article.objects.filter(is_published=True, published_at__isnull=False)
        
    #     # Filter by category if specified
    #     category_slug = self.kwargs.get('category_slug')
    #     if category_slug:hil
    #         category = get_object_or_404(Category, slug=category_slug)
    #         queryset = queryset.filter(categories=category)
        
    #     # Filter by tag if specified
    #     tag_slug = self.kwargs.get('tag_slug')
    #     if tag_slug:
    #         tag = get_object_or_404(Tag, slug=tag_slug)
    #         queryset = queryset.filter(tags=tag)
        
    #     # Search functionality
    #     query = self.request.GET.get('q')
    #     if query:
    #         queryset = queryset.filter(
    #             Q(title__icontains=query) |
    #             Q(content__icontains=query) |
    #             Q(excerpt__icontains=query)
    #         )
        
    #     return queryset.order_by('-published_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        context['featured_posts'] = Article.objects.filter(status=Article.Status.PUBLISHED)[:3]
        return context

class ArticleDetailView(generic.DetailView):
    """Individual blog post with comments"""
    model = Article
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        """Ensure only published posts are accessible"""
        return Article.objects.filter(is_published=True, published_at__isnull=False)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.filter(is_approved=True)
        context['comment_form'] = CommentForm()
        
        # Related posts by category
        categories = self.object.categories.all()
        if categories:
            context['related_posts'] = Article.objects.filter(
                is_published=True,
                categories__in=categories
            ).exclude(id=self.object.id).distinct()[:3]
        
        return context

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    """Handle comment creation (login required) [citation:9]"""
    model = Comment
    form_class = CommentForm
    template_name = 'blog/add_comment.html'
    
    def form_valid(self, form):
        """Associate comment with logged-in user and blog post"""
        form.instance.user = self.request.user
        form.instance.post = get_object_or_404(Article, 
            slug=self.kwargs['slug'], 
            is_published=True
        )
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('blog:post_detail', args=[self.kwargs['slug']])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['post'] = get_object_or_404(Article, slug=self.kwargs['slug'])
        return context