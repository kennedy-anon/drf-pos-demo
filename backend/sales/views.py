from rest_framework import generics
from rest_framework.response import Response

from Products.models import Invoices, Sales
from .serializers import SalesSerializer, creditSaleDetailSerializer, CreditSalePaymentSerializer
from api.permissions import IsAdminPermission
from payments.models import CreditSalePayment


# for viewing credit sales
class CreditSalesView(generics.ListAPIView):
    queryset = Invoices.objects.all()
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

credit_sales_view = CreditSalesView.as_view()


# for viewing credit sale detailed
class creditSaleDetailView(generics.GenericAPIView):
    permission_classes = [IsAdminPermission]

    def get(self, request, *args, **kwargs):
        invoice_no = request.query_params.get('invoice_no')
        payments = CreditSalePayment.objects.filter(invoice_no=invoice_no)
        products = Sales.objects.filter(invoice_no=invoice_no)

        payment_serializer = CreditSalePaymentSerializer(payments, many=True)
        product_serializer = creditSaleDetailSerializer(products, many=True)

        return Response({'payments': payment_serializer.data, 'products': product_serializer.data}, status=200)
    
credit_sale_detail_view = creditSaleDetailView.as_view()