from rest_framework import serializers
from Products.models import Invoices

# serialize credit sales
class SalesSerializer(serializers.ModelSerializer):
    invoice_balance = serializers.SerializerMethodField()

    class Meta:
        model = Invoices
        fields = [
            'invoice_no',
            'customer_name',
            'customer_contact_no',
            'invoice_amount',
            'invoice_paid',
            'invoice_balance',
            'created_at'
        ]

    # calculating outstanding balance
    def get_invoice_balance(self, obj):
        if obj.invoice_paid is not None:
            return obj.invoice_amount - obj.invoice_paid
        else:
            return obj.invoice_amount
        