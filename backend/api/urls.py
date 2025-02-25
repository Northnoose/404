from django.urls import path
from . import views  # Import views from the current folder

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
]
