from rest_framework import serializers

from .models import CreditSalePayment
from Products.models import Invoices

# serializing credit sales payments
class CreditSalePaymentSerializer(serializers.Serializer):
    invoice_no = serializers.PrimaryKeyRelatedField(queryset=Invoices.objects.all())
    amount = serializers.DecimalField(max_digits=14, decimal_places=2)

    class Meta:
        model = CreditSalePayment
        fields = [
            'payment_id',
            'amount',
            'invoice_no',
            'created_at'
        ]