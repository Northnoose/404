from django.urls import path
from . import views  # Import views from the current folder

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('reigster', views.register_view, name='register')
]
