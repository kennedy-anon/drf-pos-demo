from rest_framework import generics, serializers
from rest_framework.response import Response
from django.db import transaction
from django.db.models import F
from reportlab.lib.pagesizes import portrait
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate, KeepTogether
from django.http import HttpResponse
import pytz
import datetime

from .models import ProductDetail, StockLevel, PurchaseHistory, Sales, Invoices
from .serializers import ProductDetailSerializer, PurchaseHistorySerializer, PosSerializer, ProductListSerializer, ProductDetailUpdateSerializer, StockLevelUpdateSerializer, ProductDeleteSerializer, StockLevelLowSerializer, StockLevelUpdateOpeningStockSerializer
from api.permissions import IsAdminPermission, IsCashier

# for listing products running low on stock
class StockLowAPIView(generics.ListAPIView):
    queryset = StockLevel.objects.filter(available_units__lte=F('min_units_alert'))
    serializer_class = StockLevelLowSerializer
    permission_classes = [IsAdminPermission]

stock_low_view = StockLowAPIView.as_view()


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


# updating available units
class UpdateAvailableUnitsView(generics.UpdateAPIView):
    serializer_class = StockLevelUpdateOpeningStockSerializer
    permission_classes = [IsAdminPermission]

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = self.kwargs['product_id']
        available_units = serializer.validated_data.pop('available_units')

        stock_level = StockLevel.objects.get(product_id=product_id)
        stock_level.available_units = available_units
        stock_level.save()

        return Response({'detail': 'Stock updated successfully.'}, status=200)

update_available_units_view = UpdateAvailableUnitsView.as_view()


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


# deleting a product
class ProductDeleteAPIView(generics.DestroyAPIView):
    queryset = ProductDetail.objects.all()
    serializer_class = ProductDeleteSerializer
    lookup_field = 'product_id'
    permission_classes = [IsAdminPermission]

    def perform_destroy(self, instance):
        instance.delete()

product_delete_view = ProductDeleteAPIView.as_view()


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
        logged_in_user = self.request.user
        username = logged_in_user.username

        products_data = serializer.validated_data.pop('products')
        invoice_data = serializer.validated_data.pop('invoice')
        sale_type = serializer.validated_data.pop('sale_type')
        total_sales = serializer.validated_data.pop('total_sales')
        cash_received = serializer.validated_data.pop('cash_received') if serializer.validated_data.get('cash_received') is not None else ''
        change = serializer.validated_data.pop('change') if serializer.validated_data.get('change') is not None else ''

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
            receipt_pdf = self.generate_receipt_pdf(products_data, total_sales, cash_received, change, username)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="sales_receipt.pdf"'
            response.write(receipt_pdf)
            return response

        return Response({'detail': 'Sale added successfully.'}, status=201)
    
    def generate_receipt_pdf(self, products_data, total_sales, cash_received, change, username):
        doc = SimpleDocTemplate("sales_receipt.pdf", pagesize=portrait((226.08, 841.89)), leftMargin=0,
                    rightMargin=0,
                    topMargin=14.17,
                    bottomMargin=0,)

        elements = []

        styles = getSampleStyleSheet()
        styles['Heading5'].fontName = 'Helvetica'
        styles['Heading5'].alignment = TA_CENTER
        styles['Heading5'].spaceAfter = 0
        styles['Heading5'].spaceBefore = 3

        elements.append(Paragraph("Kenloy Investments", styles['Heading5']))
        elements.append(Paragraph("P.O. BOX 10300", styles['Heading5']))
        elements.append(Paragraph("KERUGOYA", styles['Heading5']))

        styles['Heading5'].fontName = 'Helvetica-Bold'
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("Sales Receipt", styles['Heading5']))
        elements.append(Spacer(1, 6))

        current_time = get_current_time()
        styles['Heading6'].fontName = 'Helvetica'
        elements.append(Paragraph(f"Date: {current_time.strftime('%d/%m/%Y')} {current_time.strftime('%I:%M %p')}", styles['Heading6']))
        elements.append(Paragraph(f"Cashier: {username.capitalize()}", styles['Heading6']))
        elements.append(Spacer(1, 6))

        styles['Normal'].fontSize = 7
        product_name_style = ParagraphStyle(
            name='product_name_style',
            fontName='Helvetica',
            fontSize=7,
            alignment=TA_LEFT,
            spaceAfter=0,
            spaceBefore=0,
        )

        # Convert products_data to a list of rows for the table
        table_data = [["Product Name", "Price", "", "Amount"]]
        for product in products_data:
            row = [Paragraph(product['product_name'], product_name_style), str(product['unitPrice']), f"x{str(product['units'])}", str(product['amount'])]
            table_data.append(row)

        spacer_row = ["", "--------------------", "", "---------"]
        table_data.append(spacer_row)
        total_row = ["", "Total", "", Paragraph(str(total_sales), styles['Normal'])]
        table_data.append(total_row)
        cash_row = ["", "Cash Received", "", Paragraph(str(cash_received), styles['Normal'])]
        table_data.append(cash_row)
        change_row = ["", "Change", "", Paragraph(str(change), styles['Normal'])]
        table_data.append(change_row)

        table = Table(table_data, colWidths=[116, 40, 20, 50])
        style = TableStyle([
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 1),
            ('FONTSIZE', (0, 0), (-1, -1), 7),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 0),
        ])

        table.setStyle(style)
        elements.append(table)

        styles['Normal'].alignment = TA_CENTER
        elements.append(Spacer(1, 6))
        elements.append(Paragraph("________________________________", styles['Normal']))
        elements.append(Paragraph("Thank you for shopping with us.", styles['Normal']))
        elements.append(Spacer(1, 6))

        page_frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='normal')
        main_template = PageTemplate(frames=[page_frame])
        doc.addPageTemplates(main_template)

        doc.build(elements)
        with open("sales_receipt.pdf", "rb") as pdf_file:
            pdf_content = pdf_file.read()

        return pdf_content
    
pos_view = PosCreateAPIView.as_view()


# save a sale
def saveSale(invoice_no, products_data, sale_type):
    for product_data in products_data:
        product_id = product_data.pop('product_id')
        sale = Sales.objects.create(product_id=product_id, sale_type=sale_type, invoice_no=invoice_no, units=product_data['units'], amount=product_data['amount'])

        # update the stock level
        stock_level = StockLevel.objects.get(product_id=product_id)
        stock_level.available_units -= sale.units
        stock_level.save()


# get current time
def get_current_time():
        nairobi_tz = pytz.timezone('Africa/Nairobi')
        current_time = datetime.datetime.now(nairobi_tz)

        return current_time