from django.shortcuts import render, redirect

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import EmailAuthenticationForm
from django.views import View
# Create your views here.
# views.py


class EmailLoginView(LoginView):
    # Descomentar para autenticar con email
    # form_class = EmailAuthenticationForm
    
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('admin_ssu:home')
        return super().dispatch(request, *args, **kwargs)
    
    
class HomePageView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'admin_ssu/home.html')
    