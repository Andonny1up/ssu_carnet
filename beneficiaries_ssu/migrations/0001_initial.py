# Generated by Django 5.0.1 on 2024-02-13 00:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Beneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='primer nombre')),
                ('middle_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='segundo nombre')),
                ('paternal_last_name', models.CharField(max_length=50, verbose_name='apellido paterno')),
                ('maternal_last_name', models.CharField(max_length=50, verbose_name='apellido materno')),
                ('married_last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='apellido de casado')),
                ('employer_type', models.CharField(choices=[('GOB', 'Gobierno'), ('NIT', 'NIT'), ('RUC', 'RUC'), ('SUP', 'Supervisor')], max_length=3, verbose_name='tipo de empleador')),
                ('employer_id', models.CharField(max_length=50, verbose_name='número de identificación del empleador')),
                ('document_type', models.CharField(choices=[('RUN', 'RUN'), ('CI', 'Carnet de Identidad'), ('PAS', 'Pasaporte'), ('CE', 'Carnet de Extranjero')], default='CI', max_length=3, verbose_name='tipo de documento')),
                ('dni', models.CharField(max_length=15, unique=True, verbose_name='N Documento')),
                ('place_of_issue', models.CharField(blank=True, max_length=100, null=True, verbose_name='expedido en')),
                ('gender', models.CharField(choices=[('M', 'Hombre'), ('F', 'Mujer')], max_length=1, verbose_name='género')),
                ('marital_status', models.CharField(choices=[('S', 'Soltero(a)'), ('C', 'Casado(a)'), ('V', 'Viudo(a)'), ('D', 'Divorciado(a)')], max_length=1, verbose_name='estado civil')),
                ('photo', models.ImageField(upload_to='beneficiaries', verbose_name='foto')),
                ('date_of_birth', models.DateField(verbose_name='fecha de nacimiento')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='direccion')),
                ('m_code', models.CharField(max_length=10, unique=True, verbose_name='matricula')),
                ('blood_group', models.CharField(choices=[('A', 'A'), ('B', 'B'), ('AB', 'AB'), ('O', 'O')], max_length=2, verbose_name='grupo sanguíneo')),
                ('rh_factor', models.CharField(choices=[('+', 'Positivo'), ('-', 'Negativo')], max_length=1, verbose_name='factor sanguíneo')),
                ('registration_date', models.DateField(verbose_name='fecha de inscripción')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('observations', models.TextField(blank=True, verbose_name='observaciones')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beneficiary_d', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dependents', to='beneficiaries_ssu.beneficiary')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='beneficiaries_created', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updated_beneficiaries', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Carnet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_issue', models.DateField(verbose_name='fecha de emision')),
                ('date_of_expiration', models.DateField(verbose_name='fecha de vencimiento')),
                ('is_active', models.BooleanField(default=True, verbose_name='activo')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('beneficiary', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='beneficiaries_ssu.beneficiary')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='carnets_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TypeBeneficiary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='tipo de beneficiario')),
                ('can_have_dependents', models.BooleanField(default=False, verbose_name='puede tener dependientes')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='type_benef_created', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='beneficiary',
            name='type_beneficiary',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='beneficiaries_ssu.typebeneficiary'),
        ),
    ]
