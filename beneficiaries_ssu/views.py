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
        beneficiary = form.instance
        beneficiary.created_by = self.request.user
        
        # generar  m_code 
        initials_first_name = beneficiary.first_name[0:1].upper()
        initials_last_name = ''.join([x[0].upper() for x in beneficiary.last_name.split()])
        full_initials = initials_last_name + initials_first_name
        birth_day = beneficiary.date_of_birth.strftime('%d')
        birth_month = beneficiary.date_of_birth.strftime('%m')
        birth_year = beneficiary.date_of_birth.strftime('%y')
        
        m_code = birth_year + '-' + birth_month + birth_day + '-' + full_initials
        
        # comprobar si el codigo ya existe
        existings_b = Beneficiary.objects.filter(m_code__startswith=m_code)
        if existings_b.exists():
            m_code = m_code + str(existings_b.count())
        
        beneficiary.m_code = m_code
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
    

class BeneficiaryDetailView(LoginRequiredMixin, DetailView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_detail.html'
    context_object_name = 'beneficiary'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Beneficiario'
        return context