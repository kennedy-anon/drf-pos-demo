from rest_framework import generics
from rest_framework.response import Response
from django.db import transaction

from .models import CreditSalePayment
from api.permissions import IsAdminPermission
from .serializers import CreditSalePaymentSerializer
from Products.models import Invoices

# for credit sale payments
class CreditSalePaymentCreateAPIView(generics.CreateAPIView):
    queryset = CreditSalePayment.objects.all()
    serializer_class = CreditSalePaymentSerializer
    permission_classes = [IsAdminPermission]

    @transaction.atomic
    def create(self, request, *args, **kwargs):
       serializer = self.get_serializer(data=request.data)
       serializer.is_valid(raise_exception=True)

       invoice_no = serializer.validated_data['invoice_no'].invoice_no
       amount = serializer.validated_data['amount']

       invoice = Invoices.objects.select_for_update().get(invoice_no=invoice_no)
       invoice.invoice_paid = invoice.invoice_paid + amount if invoice.invoice_paid is not None else amount
       invoice.save()

       CreditSalePayment.objects.create(**serializer.validated_data)

       return Response({'detail': 'Credit sale payment added successfully.'}, status=201)
    
credit_sale_payment_view = CreditSalePaymentCreateAPIView.as_view()

