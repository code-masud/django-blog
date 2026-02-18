from django.shortcuts import render
from django.views import generic
from django.contrib.auth.models import User

# Create your views here.
class AccountsProfileView(generic.TemplateView):
    template_name = 'accounts/profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Profile | {self.request.user.username}' 
        return context