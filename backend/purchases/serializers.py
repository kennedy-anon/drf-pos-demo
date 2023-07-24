from rest_framework import serializers

from Products.models import PurchaseHistory, ProductDetail

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


# serializing all purchases
class AllPurchasesSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()

    class Meta:
        model = PurchaseHistory
        fields = [
            'product_id',
            'product_name',
            'units',
            'buying_price',
            'created_at'
        ]

    # get product name
    def get_product_name(self, obj):
        return (ProductDetail.objects.get(product_id=obj.product_id_id)).product_name