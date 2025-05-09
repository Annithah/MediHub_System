from django.urls import path
from . import views
app_name = 'auth_application'

urlpatterns = [
    path('',views.home_view,name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/',views.dashboard, name='dashboard')
]   