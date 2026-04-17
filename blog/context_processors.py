from django.db.models.functions import TruncYear, TruncMonth, TruncDay
from .models import Article
from django.db.models import Count
from .models import Category


def navbar_categories(request):
    categories = Category.alive_objects.filter(is_active=True)
    return {
        'navbar_categories': categories
    }


def archive_menu(request):
    months = (
        Article.alive_objects
        .filter(status=Article.Status.ARCHIVE)
        .annotate(month=TruncMonth("published_at"))
        .values("month")
        .annotate(total=Count("id"))
        .order_by("-month")
    )
    return {"archive_menu": months}
