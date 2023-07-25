from django.urls import path

from . import views

urlpatterns = [
    # application paths
    path('totals/', views.amounts_sum_view),
]