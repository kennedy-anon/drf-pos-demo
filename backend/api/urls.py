from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    # authentication paths
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # application paths
    path('products/', include('Products.urls')),
    path('auth/', include('user.urls')),
    path('sales/', include('sales.urls')),
    path('payments/', include('payments.urls')),
    path('purchases/', include('payments.urls')),
]