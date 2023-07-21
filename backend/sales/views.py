from rest_framework import generics

from Products.models import Invoices, Sales
from .serializers import SalesSerializer, creditSaleDetailSerializer
from api.permissions import IsAdminPermission

# for viewing credit sales
class CreditSalesView(generics.ListAPIView):
    queryset = Invoices.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

credit_sales_view = CreditSalesView.as_view()


# for viewing credit sale detailed
class creditSaleDetailView(generics.ListAPIView):
    queryset = Sales.objects.all()
    serializer_class = creditSaleDetailSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        invoice_no = self.request.query_params.get('invoice_no')
        if invoice_no is not None:
            return Sales.objects.filter(invoice_no=invoice_no)
        return super().get_queryset()

credit_sale_detail_view = creditSaleDetailView.as_view()