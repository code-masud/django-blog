from .models import Category

def navbar_categories(request):
    categories = Category.objects.filter(is_active=True)
    return{
        'navbar_categories': categories
    }