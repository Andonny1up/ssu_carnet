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

    # Usuarios
    path('users/', views.UserListView.as_view(), name='user_view'),
    path('users-search/', views.UserSearchView.as_view(), name='user-search'),
    path('users/create/', views.UserCreateView.as_view(), name='user_create'),
    path('users/edit/<int:pk>/', views.UserEditView.as_view(), name='user_edit'),
    path('users/delete_user/<int:pk>/', views.UserDeleteView.as_view(), name='delete_user'),
    path('users/detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    # Grupos
    path('groups/', views.GroupListView.as_view(), name='group_list'),
    path('groups/create/', views.GroupCreateView.as_view(), name='group_create'),
    path('groups/edit/<int:pk>/', views.GroupUpdateView.as_view(), name='group_edit'),
]