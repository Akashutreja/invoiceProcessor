from django.db import models
import datetime

# Create your models here.
class Customer(models.Model):
  name   = models.CharField(max_length=120)
  address = models.CharField(max_length=120)
  mobile_number = models.CharField(max_length=120)

class Product(models.Model):
  name   = models.CharField(max_length=120)
  price = models.FloatField()

class Invoice(models.Model):
  invoice_number = models.CharField(max_length=120, blank=True, unique=True) 
  customer = models.ForeignKey(Customer,on_delete=models.CASCADE, null=True)
  total_amount = models.IntegerField(null=True)
  product = models.ManyToManyField(Product, through='InvoiceProduct')
  due_date = models.DateTimeField(null=True)
  inovice_datetime = models.DateTimeField(default=datetime.datetime.utcnow, blank=True)
  url = models.CharField(max_length=120, blank=True)
  is_digitized = models.BooleanField(default=False)
  is_manual = models.BooleanField(default=False)

class InvoiceProduct(models.Model):
  invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  product_quantity = models.IntegerField(default=1)

