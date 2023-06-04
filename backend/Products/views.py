from rest_framework import generics

from .models import ProductDetail
from .serializers import ProductDetailSerializer

# for adding product details to the database
class ProductDetailCreateAPIView(generics.CreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    
product_create_view = ProductDetailCreateAPIView.as_view()