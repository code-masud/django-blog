from django.urls import path
from . import views


app_name = 'accounts'

urlpatterns = [
    path('profile/', views.AccountsProfileView.as_view(), name="account_profile"),
    path('contact/', views.ContactView.as_view(), name='contact'),

]