from django.core.exceptions import ValidationError
from django import forms
from .models import Category, Tag, Article, Comment

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'featured_image', 'status', 'categories', 'tags']
        widgets = {
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'is_active']
    
    def clean_name(self):
        name = (self.cleaned_data.get('name', '')).strip()
    
        if len(name) < 3:
            raise ValidationError('Category name must more then 3 characters')

        if Category.objects.filter(name__iexact=name).exclude(pk=self.instance.id).exists():
            raise ValidationError('A category with this name already exists.')

        return name
    
class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name', 'slug', 'description', 'is_active']
    
    def clean_name(self):
        name = (self.cleaned_data.get('name', '')).strip()
    
        if len(name) < 3:
            raise ValidationError('Tag name must more then 3 characters')

        if Tag.objects.filter(name__iexact=name).exclude(pk=self.instance.id).exists():
            raise ValidationError('A Tag with this name already exists.')

        return name
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']