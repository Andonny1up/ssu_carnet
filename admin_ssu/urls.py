from django.contrib.auth import views as auth_views
from django.urls import path,include
from . import views

app_name = "admin_ssu"

urlpatterns = [
    path("", views.HomePageView.as_view(), name="home"),
    # path('login/', auth_views.LoginView.as_view(), name='login'),  # redefine login
    path('login/', views.EmailLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # path('accounts/', include('django.contrib.auth.urls')),  # include other auth urls
]