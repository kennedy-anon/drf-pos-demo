from django.urls import path, include

from . import views

urlpatterns = [
    # application paths
    path('credit-sale-payment/', views.credit_sale_payment_view),
]