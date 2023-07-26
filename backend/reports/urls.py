from django.urls import path

from . import views

urlpatterns = [
    # application paths
    path('totals/', views.amounts_sum_view),
    path('products-sales-sums/', views.products_sales_report_view),
    path('sales/last-30days/', views.last_30days_sales_view),
    path('sales/monthly/', views.monthly_sales_view),
]