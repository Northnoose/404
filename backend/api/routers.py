from django.urls import path  
from backend.api.urls import urlpatterns
from .views import UserView, UserPermissionView  

urlpatterns = [
    path("users/", UserView.as_view(), name='user-list'),
    path("permissions/", UserPermissionView.as_view(), name='user-permissions')
]