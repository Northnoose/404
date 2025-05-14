from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static  
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.views.i18n import set_language
from django.utils.translation import gettext_lazy as _

from . import views
from .views import (
    blokkbasert_koding_result_view,
    profile,
    edit_profile,
    scoreboard,
    oop_quiz_view,
    oop_quiz_result_view,
    send_friend_request,
    accept_friend_request,
    reject_friend_request,
    friend_requests,
    user_search,
)

urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),  
]


urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),

    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('mark-tutorial-seen/', views.mark_tutorial_seen, name='mark_tutorial_seen'),
    
    path('modules/', views.module_overview, name='module_overview'),

    path('modules/python-lesson/', views.python_lesson_view, name='python_lesson'),
    path('modules/python-quiz/', views.python_quiz_view, name='python_quiz'),
    path('modules/python-quiz-result/', views.python_quiz_result_view, name='quiz_python_result'),

    path('modules/drag-and-drop-lesson/', views.drag_and_drop_lesson_view, name='drag_and_drop_lesson'),
    path('modules/drag-and-drop-exercise/', views.drag_and_drop_exercise_view, name='drag_and_drop_exercise'),
    path('modules/drag-and-drop-result/', views.drag_and_drop_result_view, name='drag_and_drop_result'),

    path('blokkbasert-instruksjoner/', views.blokkbasert_instruksjoner, name='blokkbasert_instruksjoner'),
    path('blokkbasert-koding/', views.blokkbasert_koding, name='block_coding_module'),
    path('blokkbasert-koding/result/', blokkbasert_koding_result_view, name='blokkbasert_koding_result'),

    path('modules/oop-lesson/', views.lesson_oop_view, name='lesson_oop'),
    path('modules/oop-quiz/', oop_quiz_view, name='quiz_oop'),
    path('modules/oop-quiz-result/', oop_quiz_result_view, name='quiz_oop_result'),

    path('friend-request/send/<int:user_id>/', send_friend_request, name='send_friend_request'),
    path('friend-request/accept/<int:request_id>/', accept_friend_request, name='accept_friend_request'),
    path('friend-request/reject/<int:request_id>/', reject_friend_request, name='reject_friend_request'),
    path('friend-requests/', friend_requests, name='friend_requests'),
    path('remove-friend/<int:friendship_id>/', views.remove_friend, name='remove_friend'),

    path('user-search/', user_search, name='user_search'),
    path('friends/progression/', views.friend_progression, name='friend_progression'), 

    path('scoreboard/', scoreboard, name='scoreboard'),
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
