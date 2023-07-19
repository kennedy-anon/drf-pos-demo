from django.urls import path, include

from . import views

urlpatterns = [
    # application paths
    path('credit-sales/', views.credit_sales_view),
    path('credit-sales/detail/', views.credit_sale_detail_view)
]