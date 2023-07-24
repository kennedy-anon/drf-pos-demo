from rest_framework import generics, serializers
from rest_framework.response import Response
from django.db import transaction


from .models import ProductDetail, StockLevel, PurchaseHistory, Sales, Invoices
from .serializers import ProductDetailSerializer, PurchaseHistorySerializer, PosSerializer, ProductListSerializer, ProductDetailUpdateSerializer, StockLevelUpdateSerializer
from api.permissions import IsAdminPermission, IsCashier

# for updating ProductDetail and StockLevel model
class ProductDetailUpdateAPIView(generics.UpdateAPIView):
    serializer_class = ProductDetailUpdateSerializer
    permission_classes = [IsAdminPermission]

    def get_object(self):
        product_id = self.kwargs['product_id']
        product_detail = ProductDetail.objects.get(product_id=product_id)
        return product_detail
    
    @transaction.atomic
    def perform_update(self, serializer):
        serializer.save()  # updating product detail

        product_id = self.kwargs['product_id']
        stock_level = StockLevel.objects.get(product_id=product_id)

        stock_level_serializer = StockLevelUpdateSerializer(stock_level, data=self.request.data, partial=True)

        if stock_level_serializer.is_valid():
            stock_level_serializer.save()
        else:
            raise serializers.ValidationError(stock_level_serializer.errors)
        
product_update_view = ProductDetailUpdateAPIView.as_view()


# for adding product details to the database
class ProductDetailCreateAPIView(generics.CreateAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDetailSerializer
    permission_classes = [IsAdminPermission]

    def perform_create(self, serializer):
        product_detail = serializer.save()
        product_id = product_detail.product_id

        # check if the product exists in the StockLevel
        try:
            stock_level = StockLevel.objects.get(product_id=product_id)
        except StockLevel.DoesNotExist:
            # create an entry if the product does not exist
            stock_level = StockLevel(product_id=product_detail, available_units=0, min_units_alert=3)
            stock_level.save()
    
product_create_view = ProductDetailCreateAPIView.as_view()


# for listing products
class ProductListAPIView(generics.ListAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductListSerializer
    permission_classes = [IsAdminPermission]

product_list_view = ProductListAPIView.as_view()


# for storing purchase history and updating stock level
class PurchaseHistoryCreateAPIView(generics.CreateAPIView):
    queryset = PurchaseHistory.objects.all()
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAdminPermission]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)

        for validated_data in serializer.validated_data:
            product_id = validated_data.pop('product_id')
            purchase_history =  PurchaseHistory.objects.create(product_id=product_id, **validated_data)

            # update the stock level
            stock_level = StockLevel.objects.get(product_id=product_id)
            stock_level.available_units += purchase_history.units
            stock_level.save()

        return Response({'detail': 'Purchases saved successfully.'}, status=201)


purchase_history_create_view =  PurchaseHistoryCreateAPIView.as_view()


# point of sale
class PosCreateAPIView(generics.CreateAPIView):
    queryset = Sales.objects.all()
    serializer_class = PosSerializer
    permission_classes = [IsCashier]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        products_data = serializer.validated_data.pop('products')
        invoice_data = serializer.validated_data.pop('invoice')
        sale_type = serializer.validated_data.pop('sale_type')
        total_sales = serializer.validated_data.pop('total_sales')
        cash_received = serializer.validated_data.pop('cash_received')
        change = serializer.validated_data.pop('change')

        if (sale_type == 'credit'):
            # handle credit sales
            invoice = Invoices.objects.create(**invoice_data)
            invoice_no = invoice.invoice_no
            saveSale(invoice, products_data, sale_type)
        elif (sale_type == 'cash'):
            # handle cash sales
            invoice_no = None
            saveSale(invoice_no, products_data, sale_type)

        # generate sale receipt

        return Response({'detail': 'Sale added successfully.'}, status=201)
    
pos_view = PosCreateAPIView.as_view()


# save a sale
def saveSale(invoice_no, products_data, sale_type):
    for product_data in products_data:
        product_id = product_data.pop('product_id')
        sale = Sales.objects.create(product_id=product_id, sale_type=sale_type, invoice_no=invoice_no, **product_data)

        # update the stock level
        stock_level = StockLevel.objects.get(product_id=product_id)
        stock_level.available_units -= sale.units
        stock_level.save()
