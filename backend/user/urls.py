from django.urls import path

from . import views

urlpatterns = [
    path('user/', views.retrieve_user_view),
    path('user/access-groups/', views.access_groups_view),
    path('user/create-new/', views.create_user_view),
    path('user/update/', views.update_user_view),
    path('user/list/', views.list_users_view),
    path('user/<int:user_id>/delete/', views.delete_user_view),
    path('user/<int:user_id>/change-password/', views.change_password_view),
    path('user/change-my-password/', views.change_my_password_view),
]