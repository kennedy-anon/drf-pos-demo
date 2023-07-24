from rest_framework import generics

from .serializers import PurchaseHistorySerializer
from api.permissions import IsAdminPermission
from Products.models import PurchaseHistory


# returns purchase history for a certain product
class PurchaseHistoryListView(generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return PurchaseHistory.objects.filter(product_id=product_id)

purchase_list_view = PurchaseHistoryListView.as_view()