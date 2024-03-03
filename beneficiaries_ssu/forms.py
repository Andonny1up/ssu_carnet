from django import forms
from .models import TypeBeneficiary, Beneficiary, Carnet, Institution

class TypeBeneficiaryForm(forms.ModelForm):
    class Meta:
        model = TypeBeneficiary
        fields = ['name','can_have_dependents']
        labels = {'name':'Descripción','can_have_dependents':'Puede tener dependientes'}
        widgets = {'name':forms.TextInput(attrs={'class':'form-control'}),
                   'can_have_dependents':forms.CheckboxInput(attrs={'class':'form-check-input'})}


class BeneficiaryForm(forms.ModelForm):
    class Meta:
        model = Beneficiary
        # fields = '__all__'
        fields = ['institution','first_name','middle_name','paternal_last_name','maternal_last_name','married_last_name',
                  'employer_type', 'employer_id','document_type','dni','place_of_issue',
                  'gender','marital_status','photo',
                  'date_of_birth','address','blood_group','rh_factor',
                  'registration_date','type_beneficiary','observations']
        
        labels = {'institution':'institución','first_name':'Nombre','middle_name':'Segundo Nombre','paternal_last_name':'Apellido Paterno','maternal_last_name ':'Apellido Materno','married_last_name':'Apellido de Casado',
                  'dni':'N# Documento','photo':'Foto','date_of_birth':'Fecha de Nacimiento','address':'Dirección','blood_group':'Grupo Sanguineo','type_beneficiary':'Tipo de Beneficiario'}
        
        widgets = {'institution': forms.Select(attrs={'class': 'form-control'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'employer_type': forms.RadioSelect(attrs={'class': 'RadioSelect'}),
                   'document_type': forms.RadioSelect(attrs={'class': 'RadioSelect'}),
                   'dni':forms.TextInput(attrs={'class':'form-control'}),
                   'place_of_issue':forms.TextInput(attrs={'class':'form-control'}),
                   'gender': forms.RadioSelect(attrs={'class': 'RadioSelect'}),
                   'marital_status': forms.RadioSelect(attrs={'class': 'RadioSelect'}),
                   'photo':forms.FileInput(attrs={'class':'form-control'}),
                   'date_of_birth':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'address':forms.TextInput(attrs={'class':'form-control'}),
                   'registration_date':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'type_beneficiary':forms.Select(attrs={'class':'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['institution'].queryset = Institution.objects.filter(deleted_at__isnull=True)
        

class CarnetForm(forms.ModelForm):
    class Meta:
        model = Carnet
        fields = ['date_of_issue', 'date_of_expiration']
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'date_of_expiration': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
        }
        

class BeneficiarySearchForm(forms.Form):
    dni = forms.CharField(max_length=15,label="Documento de identidad", widget=forms.TextInput(attrs={'class': 'form-control'}))
    birth_date = forms.DateField(label="Fecha de nacimiento",widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))