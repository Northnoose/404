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
    path('block-coding/', views.block_coding, name='block_coding_module'),
    path('modules/', views.module_overview, name='module_overview'),
    path('modules/python-lesson/', views.python_lesson_view, name='python_lesson'),
    path('modules/python-quiz/', views.python_quiz_view, name='python_quiz'),
    path('modules/python-quiz-result/', views.python_quiz_result_view, name='quiz_python_result')
]
