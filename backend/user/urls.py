from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.retrieve_user_view),
    path('user/access-groups/', views.access_groups_view),
    path('user/create-new/', views.create_user_view),
    path('user/update/', views.update_user_view),
    
]