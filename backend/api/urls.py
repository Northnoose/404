from django.urls import path
from . import views  # Import views from the current folder
from django.conf import settings
from django.conf.urls.static import static  # Import static to serve static files
from django.urls import path
from .views import profile, edit_profile


urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),  # Add slash here
    path('register/', views.register_view, name='register'),  # Add slash here
]

# Serve static files during development
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



urlpatterns += [
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
]

