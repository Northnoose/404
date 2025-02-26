from django.urls import path
from . import views  # Import views from the current folder

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('reigster', views.register_view, name='register')
]

# Nødvendig i utvikling for at Django skal kunne servere statiske filer (som CSS, JS, og bilder) direkte fra STATIC_URL-katalogen.
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

