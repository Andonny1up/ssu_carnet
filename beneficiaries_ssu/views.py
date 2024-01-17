from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from .models import TypeBeneficiary , Beneficiary, Carnet

from .forms import TypeBeneficiaryForm, BeneficiaryForm
from django import forms
# Create your views here.

class TypeBeneficiaryListView(LoginRequiredMixin, ListView):
    model = TypeBeneficiary
    template_name = 'beneficiaries_ssu/types/type_beneficiary_list.html'
    context_object_name = 'type_beneficiaries'
    paginate_by = 10
    
    def get_queryset(self):
        return TypeBeneficiary.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Beneficiarios'
        return context


class TypeBeneficiaryCreateView(LoginRequiredMixin, CreateView):
    model = TypeBeneficiary
    form_class = TypeBeneficiaryForm
    template_name = 'beneficiaries_ssu/types/type_beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:type_b_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Tipo de Beneficiario'
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class TypeBeneficiaryEditView(LoginRequiredMixin, UpdateView):
    model = TypeBeneficiary
    form_class = TypeBeneficiaryForm
    template_name = 'beneficiaries_ssu/types/type_beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:type_b_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Tipo de Beneficiario'
        return context
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)


class TypeBeneficiaryDeleteView(LoginRequiredMixin, DeleteView):
    model = TypeBeneficiary
    success_url = reverse_lazy('admin_ssu:bene_ssu:type_b_list')


# beneficiary
class BeneficiaryListView(LoginRequiredMixin, ListView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_list.html'
    context_object_name = 'beneficiaries'
    paginate_by = 10
    
    def get_queryset(self):
        return Beneficiary.objects.all().order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Beneficiarios'
        return context


class BeneficiaryCreateView(LoginRequiredMixin, CreateView):
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:b_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Beneficiario'
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


class BeneficiaryEditView(LoginRequiredMixin, UpdateView):
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:b_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Beneficiario'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dob = form.initial['date_of_birth']
        form.initial['date_of_birth'] = dob.strftime('%Y-%m-%d')
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'class':'form-control','type': 'date'})
        return form
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)