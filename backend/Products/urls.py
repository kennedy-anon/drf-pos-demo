from django.urls import path, include

from . import views

urlpatterns = [
    # application paths
    path('', views.product_create_view),
    path('new-stock/', views.purchase_history_create_view),
    path('pos/', views.pos_view),
    path('list/', views.product_list_view)
]