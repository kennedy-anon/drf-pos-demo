from rest_framework import serializers

from Products.models import PurchaseHistory

# serializes purchase history
class PurchaseHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = PurchaseHistory
        fields = [
            'product_id',
            'units',
            'buying_price',
            'created_at'
        ]