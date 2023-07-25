from django.urls import path

from . import views

urlpatterns = [
    # application paths
    path('totals/', views.amounts_sum_view),
    path('products-sales-sums/', views.products_sales_report_view),
]