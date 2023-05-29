from rest_framework import generics

from .models import Product
from .serializers import ProductSerializer

# for adding new products to the database
class ProductCreateAPIView(generics.CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
product_create_view = ProductCreateAPIView.as_view()