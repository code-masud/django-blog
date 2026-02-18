from .models import Category

def navbar_categories(request):
    categories = Category.objects.filter(is_active=True)
    return{
        'navbar_categories': categories
    }

from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from django.db.models import Count
from .models import Article

def archive_menu(request):
    months = (
        Article.objects
        .filter(status=Article.Status.ARCHIVE)
        .annotate(month=TruncMonth("created_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("-month")
    )
    return {"archive_menu": months}