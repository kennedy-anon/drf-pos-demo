from rest_framework import serializers

from Products.models import Sales


# serializing sales
class SalesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sales
        fields = [
            'product_id',
            'units',
            'amount',
            'sale_type',
            'invoice_no',
            'created_at'
        ]