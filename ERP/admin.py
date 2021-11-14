from django.contrib import admin
from ERP.models import *


@admin.register(ImportedCars)
class ImportedCarsAdmin(admin.ModelAdmin):
    list_display = ['vin_code', 'import_date', 'model', 'make', 'color']


@admin.register(Parts)
class PartsAdmin(admin.ModelAdmin):
    list_display = ['part_name', 'part_number']
    search_fields = ['part_number']

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ['car', 'part_name', 'part_number', 'barcode', 'selling_price', 'note']
    autocomplete_fields = ['part_number']
    search_fields = ['barcode']
    # readonly_fields = ['part_name']