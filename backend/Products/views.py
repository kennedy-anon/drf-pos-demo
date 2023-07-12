from rest_framework import generics
from rest_framework.response import Response

from .models import ProductDetail, StockLevel, PurchaseHistory
from .serializers import ProductDetailSerializer, PurchaseHistorySerializer
from api.permissions import IsAdminPermission

# for adding product details to the database
class ProductDetailCreateAPIView(generics.CreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminPermission]

    def perform_create(self, serializer):
        product_detail = serializer.save()
        product_id = product_detail.product_id

        # check if the product exists in the StockLevel
        try:
            stock_level = StockLevel.objects.get(product_id=product_id)
        except StockLevel.DoesNotExist:
            # create an entry if the product does not exist
            stock_level = StockLevel(product_id=product_detail, available_units=0, min_units_alert=3)
            stock_level.save()
    
product_create_view = ProductDetailCreateAPIView.as_view()


# for storing purchase history and updating stock level
class PurchaseHistoryCreateAPIView(generics.CreateAPIView):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAdminPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        for validated_data in serializer.validated_data:
            product_id = validated_data.pop('product_id')
            purchase_history =  PurchaseHistory.objects.create(product_id=product_id, **validated_data)

            # update the stock level
            stock_level = StockLevel.objects.get(product_id=product_id)
            stock_level.available_units += purchase_history.units
            stock_level.save()

        return Response({'detail': 'Purchases saved successfully.'}, status=201)


purchase_history_create_view =  PurchaseHistoryCreateAPIView.as_view()