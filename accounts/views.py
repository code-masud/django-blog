
from django.views import generic
from django.contrib import messages
from .forms import ContactForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class AccountsProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'accounts/profile.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Profile | {self.request.user.username}' 
        return context
    
class ContactView(generic.FormView):
    template_name = 'accounts/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy('accounts:contact')

    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Thank you for your message! We will contact with you soon.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Contact'
        return context