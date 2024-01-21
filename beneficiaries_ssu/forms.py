from django import forms
from .models import TypeBeneficiary, Beneficiary, Carnet

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
        fields = ['first_name','last_name','dni','photo','date_of_birth','address','blood_group','type_beneficiary']
        labels = {'first_name':'Nombre(s)','last_name':'Apellidos','dni':'C.I.','photo':'Foto','date_of_birth':'Fecha de Nacimiento','address':'Dirección','blood_group':'Grupo Sanguineo','type_beneficiary':'Tipo de Beneficiario'}
        widgets = {'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'last_name':forms.TextInput(attrs={'class':'form-control'}),
                   'dni':forms.TextInput(attrs={'class':'form-control'}),
                   'photo':forms.FileInput(attrs={'class':'form-control'}),
                   'date_of_birth':forms.DateInput(attrs={'class':'form-control', 'type':'date'}),
                   'address':forms.TextInput(attrs={'class':'form-control'}),
                   'blood_group':forms.TextInput(attrs={'class':'form-control'}),
                   'type_beneficiary':forms.Select(attrs={'class':'form-control'}),
        }
        

class CarnetForm(forms.ModelForm):
    class Meta:
        model = Carnet
        fields = ['date_of_issue', 'date_of_expiration']
        widgets = {
            'date_of_issue': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
            'date_of_expiration': forms.DateInput(attrs={'class':'form-control', 'type': 'date'}),
        }