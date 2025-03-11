from django.urls import path
from . import views  
from django.conf import settings
from django.conf.urls.static import static  
from django.urls import path
from .views import profile, edit_profile


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('register/', views.register_view, name='register'), 
    path('profile/', views.profile, name='profile'),  
    path('profile/edit/', views.edit_profile, name='edit_profile'),  
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += [
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    # Ny rute for moduloversikt
    path('modules/', views.module_overview, name='module_overview'),
]