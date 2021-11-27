from rest_framework import serializers

from .models import Stock, Sales


class StockSerializers(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['car', 'part_name', 'part_number', 'barcode', 'note', 'selling_price', 'amount_in_stock', 'shelf']


class SalesSerializers(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['car_id', 'part_number_id', 'barcode', 'note', 'price', 'sell_date']