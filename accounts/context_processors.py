from .models import Company

def company_data(request):
    return {
        'company_data': Company.objects.first()
    }