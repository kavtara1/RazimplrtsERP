import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import random


class ImportedCars(models.Model):
    vin_code = models.CharField(default=None, max_length=10)
    import_date = models.DateField()
    model = models.CharField(default=None, max_length=10)
    make = models.CharField(default=None, max_length=10)
    color = models.CharField(default=None, max_length=20, null=True)

    class Meta:
        verbose_name = 'ImportedCar'
        verbose_name_plural = 'ImportedCars'

    def __str__(self):
        return self.vin_code


class Parts(models.Model):
    part_number = models.CharField(unique=True, max_length=150)
    part_name = models.CharField(default=None, max_length=10)

    class Meta:
        verbose_name = 'Part'
        verbose_name_plural = 'Parts'

    def __str__(self):
        return str(self.part_number)


class Stock(models.Model):
    car = models.ForeignKey(ImportedCars, default=None, on_delete=models.PROTECT)
    part_name = models.CharField(default=None, max_length=100, blank=True)
    part_number = models.ForeignKey(Parts, default=None, on_delete=models.PROTECT)
    barcode = models.IntegerField(default=random.randint(111111111, 999999999), unique=True)
    note = models.TextField(default=None)
    selling_price = models.IntegerField(default=0)
    amount_in_stock = models.IntegerField(default=1)
    shelf = models.CharField(max_length=10, default=1)


@receiver(post_save, sender=Stock, dispatch_uid="update_part_number")
def update_part_number(sender, **kwargs):
    obj1 = Stock.objects.last()
    part_number = getattr(obj1, 'part_number')
    obj2 = Parts.objects.filter(part_number=part_number).values('part_name')
    part_name_value = (obj2[0]['part_name'])
    x = Stock.objects.latest('id')
    latest_id = x.id
    Stock.objects.filter(id=latest_id).update(part_name=part_name_value)


class Sales(models.Model):
    car_id = models.IntegerField(default=0, blank=False)
    part_number_id = models.IntegerField(default=0,blank=False)
    barcode = models.IntegerField(default=0, blank=False)
    note = models.CharField(max_length=100, blank=True, default=None)
    price = models.IntegerField(default=0, blank=False)
    sell_date = models.DateField(default=datetime.date.today())



