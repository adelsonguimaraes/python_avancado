from basic import models
from django.db.models import OuterRef, Subquery, Exists


# Atividade 38: exemplo de subquery
def product_last_sale_date():
    sbq = models.SaleItem.objects.select_related('sale').filter(product=OuterRef('id'))\
              .values('sale__date').order_by('-sale_date')[:1]

    products = models.Product.objects.annotate(last_sale=Subquery(sbq)).values('id', 'name', 'last_sale')
    for p in products:
        print(f"{p['id']} - {p['name']} - {p['last_sale']}")


# Atividade 39: trazer produtos que tiveram alguma venda no ano de 2022
def product_sale_in_year(year):
    sbq = models.SaleItem.objects.select_related('sale').filter(product=OuterRef('id'), sale__date__year=year)\
              .values('sale__date')[:1]
    products = models.Product.objects.annotate(exists=Exists(sbq)).values('id', 'name', 'exists')
    for p in products:
        print(f"{p['name']} - {p['exists']}")


# Atividade 40: exemplo utilizando IN
def example_with_in():
    sbq = models.SaleItem.objects.filter(sale__date__year=2021).values_list('product', flat=True).distinct()
    products = models.Product.objects.filter(id__in=sbq).values('id', 'name')
    for p in products:
        print(f"{p['id']} - {p['name']}")



