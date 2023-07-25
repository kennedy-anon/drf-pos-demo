from rest_framework import generics
from django.db.models import Sum
from rest_framework.response import Response
from dateutil.parser import parse

from purchases.serializers import PurchaseHistorySerializer
from Products.models import PurchaseHistory
from api.permissions import IsAdminPermission


class AmountsSumAPIView(generics.ListAPIView):
    serializer_class = PurchaseHistorySerializer
    permission_classes = [IsAdminPermission]

    def get_queryset(self):
        start_date_str = self.request.query_params.get('start_date')
        end_date_str = self.request.query_params.get('end_date')

        if not start_date_str or not end_date_str:
            return PurchaseHistory.objects.none()
        
        try:
            start_date = parse(start_date_str)
            end_date = parse(end_date_str)
        except ValueError:
            return PurchaseHistory.objects.none()
        
        totalPurchases = PurchaseHistory.objects.filter(created_at__range=(start_date, end_date)).aggregate(Sum('buying_price'))['buying_price__sum']
        print(totalPurchases)

        return totalPurchases
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        if queryset is None:
            return Response({'detail': 'Invalid date format or missing dates.'}, status=400)
        
        return Response({'total_purchases': queryset}, status=200)
    
amounts_sum_view = AmountsSumAPIView.as_view()
