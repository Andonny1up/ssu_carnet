from django.urls import path,include
from . import views

app_name = "bene_ssu"

urlpatterns = [
    path("type_beneficiaries", views.TypeBeneficiaryListView.as_view(), name="type_b_list"),
    path("type_beneficiaries/create/", views.TypeBeneficiaryCreateView.as_view(), name="type_b_create"),
    path("type_beneficiaries/edit/<int:pk>/", views.TypeBeneficiaryEditView.as_view(), name="type_b_edit"),
    path("type_beneficiaries/delete/<int:pk>/", views.TypeBeneficiaryDeleteView.as_view(), name="type_b_delete"),

    # beneficiaries
    path("beneficiaries", views.BeneficiaryListView.as_view(), name="b_list"),
    path("beneficiaries/create/", views.BeneficiaryCreateView.as_view(), name="b_create"),
    path("beneficiaries/edit/<int:pk>/", views.BeneficiaryEditView.as_view(), name="b_edit"),
    path("beneficiaries/detail/<int:pk>/", views.BeneficiaryDetailView.as_view(), name="b_detail"),
    
]
