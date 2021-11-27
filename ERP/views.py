from django.shortcuts import render
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Stock, Sales
from .serializers import StockSerializers, SalesSerializers
from django.db.models import Count, Sum


class StockAPIView(APIView):
    serializer_class = StockSerializers

    def get_queryset(self):
        items = Stock.objects.all()
        return items

    def get(self, request, *args, **kwargs):
        try:
            barcode = request.query_params['barcode']

            if barcode:
                item = Stock.objects.get(barcode=barcode)
                serializer = StockSerializers(item)
        except:
            items = self.get_queryset()
            serializer = StockSerializers(items, many=True)

        return Response(serializer.data)


class SalesAPIView(APIView):
    serializer_class = SalesSerializers

    def get_queryset(self):
        items = Sales.objects.all()
        return items

    def get(self, request, *args, **kwargs):
        car_id = request.query_params['car_id']
        if car_id:
            sales = Sales.objects.filter(car_id=car_id)
            serializer = SalesSerializers(sales, many=True)
        else:
            sales = Sales.objects.filter(car_id=car_id)
            serializer = SalesSerializers(sales, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sale_data = request.data
        new_sale = Sales.objects.create(car_id=sale_data['car_id'], part_number_id=sale_data['part_number_id'], barcode=
                    sale_data['barcode'], note=sale_data['note'], price=sale_data['price'])
        new_sale.save()
        sold_item_barcode = sale_data["barcode"]
        reduce_amount = Stock.objects.get(barcode=sold_item_barcode)
        final_amount = reduce_amount.amount_in_stock - 1
        Stock.objects.filter(barcode=sold_item_barcode).update(amount_in_stock=final_amount)
        serializer = SalesSerializers(new_sale)
        return Response(serializer.data)


class ReportsApiView(APIView):
    serializer_class = SalesSerializers

    def get_queryset(self):
        reports = Sales.objects.all()
        return reports

    def get(self, request, *args, **kwargs):
        full_amount_sold_per_car = None
        try:
            car_id = request.query_params['car_id']

            if car_id:
                sold_per_car = Sales.objects.all().filter(car_id=car_id)
                full_amount_sold_per_car = Sales.objects.all().filter(car_id=car_id).aggregate(Sum('price'))
                serializer = SalesSerializers(sold_per_car, many=True)
        except:
            items = self.get_queryset()
            serializer = SalesSerializers(items, many=True)

        return Response(
            {'sum': full_amount_sold_per_car if full_amount_sold_per_car else 0, 'objects': serializer.data})
