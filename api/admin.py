from django.contrib import admin
from .models import Invoice, Product, Customer#, InvoiceProduct
# Register your models here.


admin.site.register(Invoice)
admin.site.register(Product)
admin.site.register(Customer)
# admin.site.register(InvoiceProduct)