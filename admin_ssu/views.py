from django.shortcuts import render, redirect

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User, Group
# formularios
from .forms import EmailAuthenticationForm
from . import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

#json
from django.http import JsonResponse
from django.core import serializers

# models
from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

# views
from django.contrib.auth.views import LoginView
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
# Create your views here.
# views.py
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

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
    

# Usuarios
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'admin_ssu/users/user_list.html'
    context_object_name = 'users'
    paginate_by = 10
    
    def get_queryset(self):
        return User.objects.all().order_by('-date_joined')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Usuarios'
        return context
    

class UserSearchView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '')
        if query:
            users = User.objects.annotate(
                full_name=Concat('first_name', V(' '), 'last_name')
            ).filter(Q(full_name__icontains=query) | Q(username__icontains=query))
        else:
            users = User.objects.all()
        users_json = serializers.serialize('json', users)
        return JsonResponse(users_json, safe=False)
    

class UserCreateView(LoginRequiredMixin,CreateView):
    model = User
    form_class = forms.CustomUserCreationForm
    template_name = 'admin_ssu/users/user_create.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    

class UserEditView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = forms.CustomUserEditForm
    # form_class = UserChangeForm
    template_name = 'admin_ssu/users/user_edit.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    # template_name = 'admin_ssu/users/user_confirm_delete.html'
    success_url = reverse_lazy('admin_ssu:user_view')
    

class UserDetailView(LoginRequiredMixin,DetailView):
    model = User
    template_name = 'admin_ssu/users/user_detail.html'
    context_object_name = 'user'
    
#fin usuarios

# Grupos
class GroupListView(LoginRequiredMixin,ListView):
    model = Group
    template_name = 'admin_ssu/groups/group_list.html'
    context_object_name = 'groups'
    paginate_by = 10

    
class GroupCreateView(LoginRequiredMixin,CreateView):
    model = Group
    template_name = 'admin_ssu/groups/group_add_edit.html'
    form_class = forms.GroupForm
    success_url = reverse_lazy('admin_ssu:group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_types = ContentType.objects.all().order_by('model')
        permissions_by_group = []
        for content_type in content_types:
            permissions_of_model = Permission.objects.filter(content_type=content_type)
            if permissions_of_model:
                permissions_by_group.append((content_type, permissions_of_model))
        context['permissions_by_group'] = permissions_by_group
        context['action'] = 'Crear'
        return context
    

class GroupUpdateView(LoginRequiredMixin, UpdateView):
    model = Group
    template_name = 'admin_ssu/groups/group_add_edit.html'
    form_class = forms.GroupForm
    success_url = reverse_lazy('admin_ssu:group_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        content_types = ContentType.objects.all().order_by('model')
        permissions_by_group = []
        for content_type in content_types:
            permissions_of_model = Permission.objects.filter(content_type=content_type)
            if permissions_of_model:
                permissions_by_group.append((content_type, permissions_of_model))
        context['permissions_by_group'] = permissions_by_group
        context['group_permissions'] = self.object.permissions.all()
        context['action'] = 'Editar'
        return context