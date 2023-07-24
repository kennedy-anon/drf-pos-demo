from rest_framework import serializers

from Products.models import Invoices, Sales, ProductDetail
from payments.models import CreditSalePayment

class ProductSaleSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = [
            'product_id',
            'product_name',
            'units',
            'amount',
            'sale_type',
            'invoice_no',
            'created_at'
        ]

    # get product name
    def get_product_name(self, obj):
        return (ProductDetail.objects.get(product_id=obj.product_id_id)).product_name


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
        

# serializes details of a credit view
class creditSaleDetailSerializer(serializers.ModelSerializer):
    unit_price = serializers.SerializerMethodField()
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = Sales
        fields = [
            'product_id',
            'product_name',
            'units',
            'unit_price',
            'amount',
        ]

    # calculating unit price
    def get_unit_price(self, obj):
        return obj.amount / obj.units
    
    # get product name
    def get_product_name(self, obj):
        return (ProductDetail.objects.get(product_id=obj.product_id_id)).product_name
    

# serializing credit sales payments
class CreditSalePaymentSerializer(serializers.ModelSerializer):

    class Meta:
        model = CreditSalePayment
        fields = [
            'payment_id',
            'amount',
            'created_at'
        ]
        