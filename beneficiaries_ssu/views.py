from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseRedirect

from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.urls import reverse_lazy
from .models import TypeBeneficiary , Beneficiary, Carnet

from .forms import TypeBeneficiaryForm, BeneficiaryForm, CarnetForm, BeneficiarySearchForm
from django import forms

from django.db.models import Q
from django.db.models import Value as V
from django.db.models.functions import Concat

from django.utils import timezone
from datetime import date, timedelta
# Create your views here.

# types
class TypeBeneficiaryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = TypeBeneficiary
    template_name = 'beneficiaries_ssu/types/type_beneficiary_list.html'
    context_object_name = 'type_beneficiaries'
    paginate_by = 10
    permission_required = 'beneficiaries_ssu.view_typebeneficiary'
    
    def get_queryset(self):
        queryset = TypeBeneficiary.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.filter(
                Q(name__icontains=search_query)
            )
        return queryset
    

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Tipos de Beneficiarios'
        context['search'] = self.request.GET.get('search', '')
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
class BeneficiaryListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_list.html'
    context_object_name = 'beneficiaries'
    paginate_by = 10
    permission_required = 'beneficiaries_ssu.view_beneficiary'
    
    def get_queryset(self):
        queryset = Beneficiary.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.annotate(
                full_name=Concat('first_name', V(' '), 'paternal_last_name', V(' '), 'maternal_last_name')
            ).filter(
                Q(full_name__icontains=search_query) | Q(dni__icontains=search_query)
            )
        return queryset 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Beneficiarios'
        context['search'] = self.request.GET.get('search', '')
        context['total_records'] = Beneficiary.objects.all().count()
        return context


class BeneficiaryCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:b_list')
    permission_required = 'beneficiaries_ssu.add_beneficiary'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Beneficiario'
        return context
    
    def form_valid(self, form):
        beneficiary = form.instance
        beneficiary.created_by = self.request.user
        
        # generar  m_code 
        initials_first_name = beneficiary.first_name[0:1].upper()
        initials_last_name = beneficiary.paternal_last_name[0:1].upper() + beneficiary.maternal_last_name[0:1].upper()
        # initials_last_name = ''.join([x[0].upper() for x in beneficiary.last_name.split()])
        full_initials = initials_last_name + initials_first_name
        birth_day = beneficiary.date_of_birth.strftime('%d')
        birth_month = beneficiary.date_of_birth.strftime('%m')
        birth_year = beneficiary.date_of_birth.strftime('%y')

        if beneficiary.gender == 'F':
            print('beneficiary gender: ', beneficiary.gender)
            if birth_month[:1] == '0':
                birth_month = '5' + birth_month[1:]
            else:
                birth_month = '6' + birth_month[1:]
            print('birth_month: ', birth_month)

        
        m_code = birth_year + '-' + birth_month + birth_day + '-' + full_initials
        
        # comprobar si el codigo ya existe
        existings_b = Beneficiary.objects.filter(m_code__startswith=m_code)
        if existings_b.exists():
            m_code = m_code + str(existings_b.count())
        
        beneficiary.m_code = m_code
        return super().form_valid(form)


class BeneficiaryEditView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
    success_url = reverse_lazy('admin_ssu:bene_ssu:b_list')
    permission_required = 'beneficiaries_ssu.change_beneficiary'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Beneficiario'
        return context

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        dob = form.initial['date_of_birth']
        form.initial['date_of_birth'] = dob.strftime('%Y-%m-%d')
        form.fields['date_of_birth'].widget = forms.DateInput(attrs={'class':'form-control','type': 'date'})
        
        # fecha iinscripción
        doi = form.initial['registration_date']
        form.initial['registration_date'] = doi.strftime('%Y-%m-%d')
        form.fields['registration_date'].widget = forms.DateInput(attrs={'class':'form-control','type': 'date'})
        # Si el beneficiario tiene un 'beneficiary_d', ocultamos el campo 'type_beneficiary'
        if self.object.beneficiary_d:
            form.fields['type_beneficiary'].widget = forms.HiddenInput()
            form.fields['type_beneficiary'].label = ""
        return form
    
    def form_valid(self, form):
        form.instance.updated_by = self.request.user
        return super().form_valid(form)
    

class BeneficiaryDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_detail.html'
    context_object_name = 'beneficiary'
    permission_required = 'beneficiaries_ssu.view_beneficiary'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle de Beneficiario'
        context['dependents'] = Beneficiary.objects.filter(beneficiary_d=self.object.id)
        return context


@login_required
def toggle_beneficiary_active(request, pk):
    if not request.user.has_perm('beneficiaries_ssu.change_beneficiary'):
        messages.error(request, 'No tienes permiso para cambiar este beneficiario.')
        return redirect(reverse('admin_ssu:bene_ssu:b_list'))
    
    beneficiary = get_object_or_404(Beneficiary, pk=pk)
    beneficiary.is_active = not beneficiary.is_active
    beneficiary.save()

    # Encontrar los dependientes
    dependents = Beneficiary.objects.filter(beneficiary_d=beneficiary.id)
    for dependent in dependents:
        dependent.is_active = beneficiary.is_active
        dependent.save()

    if beneficiary.is_active:
        messages.success(request, 'El beneficiario ha sido activado.')
    else:
        messages.success(request, 'El beneficiario ha sido desactivado.')

    return redirect(reverse('admin_ssu:bene_ssu:b_list')) # si necesitamos argumentos:: args=[beneficiary.id])


# Dependents
class DependentCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Beneficiary
    form_class = BeneficiaryForm
    template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
    permission_required = 'beneficiaries_ssu.add_beneficiary'
    
    def get_success_url(self):
        return reverse('admin_ssu:bene_ssu:b_detail', args=[self.object.beneficiary_d.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Dependiente'        
        return context
    
    def form_valid(self, form):
        beneficiary = form.instance
        beneficiary.beneficiary_d = Beneficiary.objects.get(id=self.kwargs['pk'])
        beneficiary.created_by = self.request.user
        
        # generar  m_code 
        initials_first_name = beneficiary.first_name[0:1].upper()
        initials_last_name = beneficiary.paternal_last_name[0:1].upper() + beneficiary.maternal_last_name[0:1].upper()
        # initials_last_name = ''.join([x[0].upper() for x in beneficiary.last_name.split()])
        full_initials = initials_last_name + initials_first_name
        birth_day = beneficiary.date_of_birth.strftime('%d')
        birth_month = beneficiary.date_of_birth.strftime('%m')
        birth_year = beneficiary.date_of_birth.strftime('%y')

        if beneficiary.gender == 'F':
            print('beneficiary gender: ', beneficiary.gender)
            if birth_month[:1] == '0':
                birth_month = '5' + birth_month[1:]
            else:
                birth_month = '6' + birth_month[1:]
            print('birth_month: ', birth_month)
        
        m_code = birth_year + '-' + birth_month + birth_day + '-' + full_initials
        
        # comprobar si el codigo ya existe
        existings_b = Beneficiary.objects.filter(m_code__startswith=m_code)
        if existings_b.exists():
            m_code = m_code + str(existings_b.count())
        
        beneficiary.m_code = m_code
        return super().form_valid(form)
    
    # def get_initial(self):
    #     initial = super().get_initial()
    #     initial['type_beneficiary'] = TypeBeneficiary.objects.get(name='Dependiente').pk
    #     return initial
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields.pop('type_beneficiary')
    #     dob = form.initial['date_of_birth']
    #     form.initial['date_of_birth'] = dob.strftime('%Y-%m-%d')
    #     form.fields['date_of_birth'].widget = forms.DateInput(attrs={'class':'form-control','type': 'date'})
        return form


# class DependentEditView(LoginRequiredMixin, UpdateView):
#     model = Beneficiary
#     form_class = BeneficiaryForm
#     template_name = 'beneficiaries_ssu/beneficiaries/beneficiary_add_edit.html'
#     success_url = reverse_lazy('admin_ssu:bene_ssu:b_list')
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Editar Dependiente'
#         return context

#     def get_form(self, form_class=None):
#         form = super().get_form(form_class)
#         form.fields.pop('type_beneficiary')
#         dob = form.initial['date_of_birth']
#         form.initial['date_of_birth'] = dob.strftime('%Y-%m-%d')
#         form.fields['date_of_birth'].widget = forms.DateInput(attrs={'class':'form-control','type': 'date'})
#         return form
    
#     def form_valid(self, form):
#         form.instance.updated_by = self.request.user
#         return super().form_valid(form)


# carnets
class BeneficiaryCarnetListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/carnets/beneficiary_carnets_list.html'
    context_object_name = 'beneficiaries'
    paginate_by = 10
    permission_required = 'beneficiaries_ssu.view_carnet'
    
    def get_queryset(self):
        queryset = Beneficiary.objects.all().order_by('-created_at')
        search_query = self.request.GET.get('search', '')
        if search_query:
            queryset = queryset.annotate(
                full_name=Concat('first_name', V(' '), 'last_name')
            ).filter(
                Q(full_name__icontains=search_query) | Q(dni__icontains=search_query)
            )
        return queryset 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carnets Beneficiarios'
        context['search'] = self.request.GET.get('search', '')
        return context
    
    
class BeneficiaryCarnetView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    model = Beneficiary
    template_name = 'beneficiaries_ssu/carnets/beneficiary_carnets.html'
    context_object_name = 'beneficiary'
    permission_required = 'beneficiaries_ssu.view_carnet'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Carnets de Beneficiario'
        carnets = Carnet.objects.filter(beneficiary=self.object).order_by('-date_of_issue')
        for carnet in carnets:
            carnet.is_expired = carnet.date_of_expiration < timezone.now().date()
            print("date_of_expiration: ", carnet.date_of_expiration)
            print("timezone.now().date(): ", timezone.now().date())
            print("timezone.now(): ", timezone.now())
            print("is_expired: ", carnet.is_expired)
        context['carnets'] = carnets
        context['active_carnet'] = Carnet.objects.filter(beneficiary=self.object, is_active=True, date_of_expiration__gte=timezone.now().date()).order_by('-date_of_issue').first()
        return context


class CarnetCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Carnet
    form_class = CarnetForm
    template_name = 'beneficiaries_ssu/carnets/carnet_add.html'
    permission_required = 'beneficiaries_ssu.add_carnet'
    
    def dispatch(self, request, *args, **kwargs):
        bene = Beneficiary.objects.get(id=self.kwargs['pk'])
        active_carnet = Carnet.objects.filter(beneficiary=bene, is_active=True, date_of_expiration__gte=timezone.now().date()).order_by('-date_of_issue').first()
        if active_carnet:
            # Si hay un carnet activo, redirige al usuario a la página que prefieras
            return HttpResponseRedirect(reverse('admin_ssu:bene_ssu:b_c_list', args=[bene.id]))
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return reverse('admin_ssu:bene_ssu:b_c_list', args=[self.object.beneficiary.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Carnet'        
        return context
    
    def form_valid(self, form):
        carnet = form.instance
        carnet.beneficiary = Beneficiary.objects.get(id=self.kwargs['pk'])
        carnet.created_by = self.request.user
        return super().form_valid(form)
    
    def get_initial(self):
        initial = super().get_initial()
        initial['date_of_issue'] = date.today().strftime('%Y-%m-%d')
        initial['date_of_expiration'] = (date.today() + timedelta(days=365)).strftime('%Y-%m-%d')
        return initial
    
    
@login_required
@permission_required('beneficiaries_ssu.delete_carnet')
def deactivate_carnet(request, pk):
    carnet = get_object_or_404(Carnet, pk=pk)
    carnet.is_active = False
    carnet.save()

    messages.success(request, 'El carnet ha sido desactivado.')
    return redirect(reverse('admin_ssu:bene_ssu:b_c_list', args=[carnet.beneficiary.id]))


class BeneficiarySearchView(View):
    def get(self, request, *args, **kwargs):
        form = BeneficiarySearchForm()
        return render(request, 'beneficiaries_ssu/carnets/beneficiary_carnet_search.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = BeneficiarySearchForm(request.POST)
        if form.is_valid():
            dni = form.cleaned_data['dni']
            birth_date = form.cleaned_data['birth_date']
            beneficiary = Beneficiary.objects.filter(dni=dni, date_of_birth=birth_date, is_active=True).first()
            print("beneficiary: ", beneficiary)
            if beneficiary:
                active_carnet = Carnet.objects.filter(beneficiary=beneficiary, is_active=True, date_of_expiration__gte=timezone.now().date()).order_by('-date_of_issue').first()
                print("active_carnet: ", active_carnet)
                if active_carnet:
                    message = 'El beneficiario tiene un carnet activo.'
                else:
                    message = 'El beneficiario no tiene un carnet activo.'
                    active_carnet = None
            else:
                message = 'No se encontró un beneficiario con los datos proporcionados.'
                active_carnet = None
                
            return render(request, 'beneficiaries_ssu/carnets/beneficiary_carnet_search.html', {'form': form, 'message': message,'active_carnet': active_carnet})
        return render(request, 'beneficiaries_ssu/carnets/beneficiary_carnet_search.html', {'form': form})