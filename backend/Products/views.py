from rest_framework import generics

from .models import ProductDetail, StockLevel
from .serializers import ProductDetailSerializer

# for adding product details to the database
class ProductDetailCreateAPIView(generics.CreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer

    def perform_create(self, serializer):
        product_detail = serializer.save()
        product_id = product_detail.product_id

        # check if the product exists in the StockLevel
        try:
            stock_level = StockLevel.objects.get(product_id=product_id)
        except StockLevel.DoesNotExist:
            # create an entry if it does not exist
            stock_level = StockLevel(product_id=product_detail, available_units=0, min_units_alert=3)
            stock_level.save()
    
product_create_view = ProductDetailCreateAPIView.as_view()