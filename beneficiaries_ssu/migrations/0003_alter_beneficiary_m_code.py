# Generated by Django 5.0.1 on 2024-02-22 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('beneficiaries_ssu', '0002_alter_beneficiary_employer_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='beneficiary',
            name='m_code',
            field=models.CharField(max_length=20, unique=True, verbose_name='matricula'),
        ),
    ]
