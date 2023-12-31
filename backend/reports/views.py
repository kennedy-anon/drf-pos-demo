from rest_framework import generics
from django.db.models import Sum
from rest_framework.response import Response
from dateutil.parser import parse
from django.db.models import F
from django.utils.timezone import timedelta
from django.utils import timezone
from datetime import datetime
import calendar

from purchases.serializers import PurchaseHistorySerializer
from Products.models import PurchaseHistory, Invoices, Sales
from api.permissions import IsAdminPermission
from .serializers import SalesSerializer


# calculates totals for purchases and sales including credit sales
class AmountsSumAPIView(generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return None
        
        try:
            start_date = parse(start_date_str)
            end_date = parse(end_date_str)
        except ValueError:
            return None
        
        totalPurchases = PurchaseHistory.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('buying_price'))['buying_price__sum']
        total_invoice_amount = Invoices.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('invoice_amount'))['invoice_amount__sum']
        total_invoice_paid = Invoices.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('invoice_paid'))['invoice_paid__sum']
        total_sales = Sales.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']

        if total_invoice_amount is not None and total_invoice_paid is not None:
            total_invoice_unpaid = total_invoice_amount - total_invoice_paid
        else:
            total_invoice_unpaid = None

        return {
            'totalPurchases': totalPurchases,
            'total_invoice_amount': total_invoice_amount,
            'total_invoice_paid': total_invoice_paid,
            'total_invoice_unpaid': total_invoice_unpaid,
            'total_sales': total_sales
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is None:
            return Response({'detail': 'Invalid date format or missing dates.'}, status=400)
        
        return Response({'totals': queryset}, status=200)
    
amounts_sum_view = AmountsSumAPIView.as_view()


# calculating totals for each product sold given certain date range
class ProductSaleReportAPIView(generics.ListAPIView):
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return None
        
        try:
            start_date = parse(start_date_str)
            end_date = parse(end_date_str)
        except ValueError:
            return None
        
        product_sales_sums = Sales.objects.filter(created_at__range=(start_date, end_date)).values('product_id', 'product_id__product_name').annotate(
            product_name=F('product_id__product_name'),
            total_amount=Sum('amount'),
            total_units=Sum('units')
        )

        return {
            'product_sales_sums': product_sales_sums
        }
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is None:
            return Response({'detail': 'Invalid date format or missing dates.'}, status=400)

        return Response({'sums': queryset}, status=200)
    
products_sales_report_view = ProductSaleReportAPIView.as_view()


# calculating sales for the last 30 days
class SaleReport30DaysAPIView(generics.ListAPIView):
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        end_date_str = self.request.query_params.get('end_date')

        if not end_date_str:
            return None
        
        try:
            end_date = parse(end_date_str)
        except ValueError:
            return None
        
        total_sales_by_day = []
        for _ in range(30):
            start_date = end_date - timedelta(days=1)
            total_sales = Sales.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']
            current_date = {
                'date': start_date,
                'total_sales': total_sales
            }
            total_sales_by_day.append(current_date)
            end_date = start_date
        
        total_sales_by_day.reverse()
        return total_sales_by_day
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is None:
            return Response({'detail': 'Invalid date format or missing endDate.'}, status=400)
        
        return Response({'total_sales_by_day': queryset}, status=200)
    
last_30days_sales_view = SaleReport30DaysAPIView.as_view()


# monthly sales report
class MonthlySalesReportAPIView(generics.ListAPIView):
    serializer_class = SalesSerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        end_date_str = self.request.query_params.get('end_date')

        if not end_date_str:
            return None
        
        try:
            end_date = parse(end_date_str)
        except ValueError:
            return None
        
        # Convert end_date to UTC
        end_date_utc = end_date.astimezone(timezone.utc)

        monthly_sales = []
        current_month = end_date_utc.month
        current_year = end_date_utc.year

        for _ in range(12):
            _, last_day_of_month = calendar.monthrange(current_year, current_month)
            start_date = datetime(current_year, current_month, 1, 21, 0, 0, tzinfo=timezone.utc) - timedelta(days=1)
            end_date = datetime(current_year, current_month, last_day_of_month, 21, 0, 0, tzinfo=timezone.utc)

            total_sales = Sales.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('amount'))['amount__sum']
            current_month_data = {
                'start_date': start_date,
                'end_date': end_date,
                'total_sales': total_sales
            }

            monthly_sales.append(current_month_data)

            # Move to the previous month
            current_month -= 1
            if current_month == 0:  # Wrap around to December and move to the previous year
                current_month = 12
                current_year -= 1


        monthly_sales.reverse()
        return monthly_sales
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is None:
            return Response({'detail': 'Invalid date format or missing endDate.'}, status=400)
        
        return Response({'monthly_sales': queryset}, status=200)
    
monthly_sales_view = MonthlySalesReportAPIView.as_view()