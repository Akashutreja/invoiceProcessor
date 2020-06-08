from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Invoice, Product, Customer, InvoiceProduct
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import datetime
# Create your views here.

@api_view(['POST'])
def invoice_create_view(request):
  if request.method == "POST":
    data = {}
    invoice_number = request.data.get("invoice_number", "")
    customer_id = request.data.get("customer_id", "")
    product_list = request.data.get("product_list", [])
    due_date = request.data.get("due_date", "")
    total_amount = request.data.get("total_amount", "")

    try:
      due_date = datetime.datetime.strptime(due_date,"%Y-%m-%d %H:%M:%S")
    except Exception as e:
      raise Exception("Due date format should be in %Y-%m-%d %H:%M:%S")
    

    #fetch customer details , 
    customer = Customer.objects.get(pk=customer_id)

    #invoice
    i1= Invoice.objects.create(invoice_number=invoice_number,customer=customer,total_amount=total_amount, due_date=due_date, is_manual=True)
    i1.save()

    for product in product_list:
      p1 = Product.objects.get(id=product['id'])
      quantity = product['quantity']
      ip = InvoiceProduct(invoice=i1, product=p1,product_quantity=quantity)
      ip.save()

    return Response({"Success": True}, status=HTTP_200_OK)


@api_view(['GET'])
def invoice_get_view(request):
  try:
    invoice_number = request.data.get("invoice_number", "")
    i1 = Invoice.objects.filter(invoice_number=invoice_number)
    if i1:
      if i1[0].is_manual or i1[0].is_digitized:
        data = {}
        data['invoice_number'] = i1[0].invoice_number
        data['customer_id'] = i1[0].customer_id
        data['due_date'] = i1[0].due_date
        data['total_amount'] = i1[0].total_amount
        data['product_list'] = []
        ip1 = InvoiceProduct.objects.filter(invoice=i1[0]).select_related('product')
        for invoice_product in ip1:
          data['product_list'].append({'id': invoice_product.product.id, 'quantity': invoice_product.product_quantity})
        return Response({"Success": True, "data": data}, status=HTTP_200_OK)
      else:
        return Response({"Success": True, "data": {}}, status=HTTP_200_OK)
    else:
      return Response({"Success": True, "data": {}}, status=HTTP_200_OK)
  except Exception as e:
    raise e

@api_view(['POST'])
def invoice_update_view(request):
  if request.method == "POST":
    data = {}
    invoice_number = request.data.get("invoice_number", None)
    data['customer_id'] = request.data.get("customer_id", None)
    product_list = request.data.get("product_list", None)
    data['due_date'] = request.data.get("due_date", None)
    data['total_amount'] = request.data.get("total_amount", None)

    data = {k: v for k, v in data.items() if v is not None}
    try:
      invoice_qs = Invoice.objects.filter(invoice_number=invoice_number)
      if invoice_qs:
        if 'customer_id' in data:
          customer = Customer.objects.get(pk=data['customer_id'])
          invoice_qs[0].customer = customer
          invoice_qs[0].save()
        if 'due_date' in data:
          try:
            data['due_date'] = datetime.datetime.strptime(data['due_date'],"%Y-%m-%d %H:%M:%S")
          except Exception as e:
            raise Exception("Due date format should be in %Y-%m-%d %H:%M:%S")

        invoice_qs.update(**data)

        if product_list:
          for product in product_list:
            p1 = Product.objects.get(id=product['id'])
            quantity = product['quantity']
            ip = InvoiceProduct(invoice=invoice_qs[0], product=p1,product_quantity=quantity)
            ip.save()
        return Response({"Success": True}, status=HTTP_200_OK)


      else:
        return Response({"Success": False, "Message": "No Invoice exist with given invoice number please check"}, status=HTTP_400_BAD_REQUEST)
        pass
    except Exception as e:
      raise e
