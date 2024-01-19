from django.db import models
from django.conf import settings
# Create your models here.

# model type of beneficiary
class TypeBeneficiary(models.Model):
    name = models.CharField('tipo de beneficiario',max_length=50)
    can_have_dependents = models.BooleanField('puede tener dependientes',default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='type_benef_created')

    def __str__(self):
        return self.name

#model beneficiary
class Beneficiary(models.Model):
    first_name = models.CharField('nombre',max_length=50)
    last_name = models.CharField('apellido',max_length=50)
    dni = models.CharField('ci',max_length=15, unique=True)
    photo = models.ImageField('foto',upload_to='beneficiaries')
    date_of_birth = models.DateField('fecha de nacimiento')
    address = models.CharField('direccion',max_length=100,null=True,blank=True)
    m_code = models.CharField('matricula',max_length=10,unique=True)
    blood_group = models.CharField('grupo sanguineo',max_length=5)
    is_active = models.BooleanField('activo',default=True)
    type_beneficiary = models.ForeignKey(TypeBeneficiary, on_delete=models.SET_NULL, null=True,blank=True)
    beneficiary_d = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='dependents')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='beneficiaries_created')
    
    def __str__(self):
        return self.first_name.upper() + ' ' + self.last_name.upper()
    

# carnet
class Carnet(models.Model):
    date_of_issue = models.DateField('fecha de emision')
    date_of_expiration = models.DateField('fecha de vencimiento')
    beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
    is_active = models.BooleanField('activo',default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='carnets_created')