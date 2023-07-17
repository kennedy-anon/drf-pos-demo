from rest_framework import generics

from Products.models import Invoices
from .serializers import SalesSerializer
from api.permissions import IsAdminPermission

# for viewing credit sales
class CreditSalesView(generics.ListAPIView):
    queryset = Invoices.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

credit_sales_view = CreditSalesView.as_view()