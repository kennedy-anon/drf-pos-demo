from django.urls import path, include

urlpatterns = [
    # application paths
    path('products/', include('Products.urls')),
]