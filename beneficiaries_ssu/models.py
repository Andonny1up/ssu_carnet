from datetime import date
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
    DOCUMENT_TYPES = [
        ('RUN', 'RUN'),
        ('CI', 'Carnet de Identidad'),
        ('PAS', 'Pasaporte'),
        ('CE', 'Carnet de Extranjero'),
    ]
    
    GENDER_CHOICES = [
        ('M', 'Hombre'),
        ('F', 'Mujer'),
    ]
    
    BLOOD_GROUP_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ]

    RH_FACTOR_CHOICES = [
        ('+', 'Positivo'),
        ('-', 'Negativo'),
    ]
    
    MARITAL_STATUS_CHOICES = [
        ('S', 'Soltero(a)'),
        ('C', 'Casado(a)'),
        ('V', 'Viudo(a)'),
        ('D', 'Divorciado(a)'),
    ]
    EMPLOYER_TYPE_CHOICES = [
        ('GOB', 'GOB'),
        ('NIT', 'NIT'),
        ('RUC', 'RUC'),
        ('SUP', 'SUP'),
    ]
    # CAMPOS
    first_name = models.CharField('primer nombre', max_length=50)
    middle_name = models.CharField('segundo nombre', max_length=50, blank=True, null=True)
    paternal_last_name = models.CharField('apellido paterno', max_length=50)
    maternal_last_name = models.CharField('apellido materno', max_length=50)
    married_last_name = models.CharField('apellido de casado', max_length=50, blank=True, null=True)
    
    employer_type = models.CharField('tipo de empleador', max_length=3, choices=EMPLOYER_TYPE_CHOICES,default='NIT')
    employer_id = models.CharField('número de identificación del empleador', max_length=50)
    
    document_type = models.CharField('tipo de documento', max_length=3, choices=DOCUMENT_TYPES, default='CI')
    dni = models.CharField('N Documento',max_length=15, unique=True)
    place_of_issue = models.CharField('expedido en', max_length=100, null=True, blank=True)
    
    gender = models.CharField('género', max_length=1, choices=GENDER_CHOICES,default='M')
    marital_status = models.CharField('estado civil', max_length=1, choices=MARITAL_STATUS_CHOICES,default='S')
    
    photo = models.ImageField('foto',upload_to='beneficiaries')
    date_of_birth = models.DateField('fecha de nacimiento')
    address = models.CharField('direccion',max_length=100,null=True,blank=True)
    m_code = models.CharField('matricula',max_length=10,unique=True)
    
    blood_group = models.CharField('grupo sanguíneo', max_length=2, choices=BLOOD_GROUP_CHOICES)
    rh_factor = models.CharField('factor sanguíneo', max_length=1, choices=RH_FACTOR_CHOICES)
    
    registration_date = models.DateField('fecha de inscripción')
    
    is_active = models.BooleanField('activo',default=True)
    type_beneficiary = models.ForeignKey(TypeBeneficiary, on_delete=models.SET_NULL, null=True,blank=True)
    beneficiary_d = models.ForeignKey('self',on_delete=models.CASCADE,blank=True,null=True,related_name='dependents')
    observations = models.TextField('observaciones', blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='beneficiaries_created')
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='updated_beneficiaries', null=True, blank=True)
    
    def __str__(self):
        return self.first_name.upper() + ' ' + self.paternal_last_name.upper()
    
    def age(self):
        today = date.today()
        born = self.date_of_birth
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    

# carnet
class Carnet(models.Model):
    date_of_issue = models.DateField('fecha de emision')
    date_of_expiration = models.DateField('fecha de vencimiento')
    beneficiary = models.ForeignKey(Beneficiary,on_delete=models.CASCADE)
    is_active = models.BooleanField('activo',default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='carnets_created')