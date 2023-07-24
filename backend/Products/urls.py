from django.urls import path, include

from . import views

urlpatterns = [
    # application paths
    path('', views.product_create_view),
    path('<int:product_id>/', views.product_update_view),
    path('<int:product_id>/delete/', views.product_delete_view),
    path('new-stock/', views.purchase_history_create_view),
    path('low-stock/', views.stock_low_view),
    path('pos/', views.pos_view),
    path('list/', views.product_list_view)
]