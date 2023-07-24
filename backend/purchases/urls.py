from django.urls import path

from . import views

urlpatterns = [
    # application paths
    path('<int:product_id>/', views.purchase_list_view),
]