from django.db.models import OuterRef, F, Subquery, Count, Sum, Value

from basic import models


# Consultar funcionários com do sexo masculino, salário igual ou acima de 1700 e do departamento Atendente
# mostrar nome, salário, departamento e distrito
def consulta01():
    employees = models.Employee.objects.select_related('department', 'district')\
        .filter(gender__exact='M', salary__gte=1700, department__name__icontains='Atendente')
    for e in employees:
        print(f"{e.name} - {e.salary} - {e.department.name} - {e.district.name}")


# Distrito, cidade e total de funcionários
def consulta02():
    sbq = models.Employee.objects.filter(district_id__exact=OuterRef('id')).values('district').annotate(
        total=Count('*')
    ).values('total')
    districts = models.District.objects.annotate(
        total=Subquery(sbq)
    ).values('name', 'city__name', 'total')
    for d in districts:
        print(f"{d['name']} - {d['city__name']} - {d['total']}")


# Produto com preço de venda >=800 e <=1500, que o documento do supplier possua 015 e que tenha venda 2019+
# apresentar o total de produtos vendidos
def consulta03():
    sbq = models.SaleItem.objects.filter(product=OuterRef('id')).values('product_id').annotate(total=Count('*')).values('total')
    products = models.Product.objects.select_related('saleitems').filter(
        cost_price__gte=800, cost_price__lte=1500,
        supplier__legal_document__icontains='015', saleitems__sale__date__year__gte=2019)\
        .annotate(total=Subquery(sbq))\
        .values('name', 'supplier__legal_document', 'saleitems__sale__date__year', 'total').distinct('id')
    for p in products:
        print(f"{p['name']} - {p['supplier__legal_document']} - {p['saleitems__sale__date__year']} - {p['total']}")


# Os 3 produtos mais vendidos no ano, receber o ano como parametro
def consulta04(year):
    sbq = models.SaleItem.objects.filter(product=OuterRef('id')).values('product_id').annotate(total=Count('*')).values('total')
    products = models.Product.objects.select_related('saleitems').filter(saleitems__sale__date__year=Value(year)).values('id').annotate(
        count=Count('id'),
        total=Subquery(sbq),
        year=F('saleitems__sale__date__year')
    ).values('id', 'name', 'total', 'year').order_by('-total')[:3]

    if not products:
        print(f'Nenhum produto localizado no ano {year}')

    for p in products:
        print(f"{p['name']} - {p['total']} - {p['year']}")


# a filial que mais vendeu
def consulta05():
    sbq = models.Sale.objects.filter(branch=OuterRef('id')).values('branch_id').annotate(
        total=Count('saleitem__id')
    ).values('total')
    branch = models.Branch.objects.annotate(
        total=Subquery(sbq)
    ).order_by('-total')[:1][0]
    print(f"{branch.name} - {branch.total}")


# total de filias por zona
def consulta06():
    zones = models.Zone.objects.annotate(
        branchs=Count('district__branch__id')
    )
    for z in zones:
        print(f"{z.name} - {z.branchs}")


# 3 funcionários que mais venderam e seus departamentos
def consulta07():
    sbq = models.Sale.objects.prefetch_related('saleitem_set').filter(employee=OuterRef('id')).values('employee__id').annotate(
        total=Count('saleitem__id')
    ).values('total')

    employees = models.Employee.objects.select_related('department', 'district').annotate(
        total_sales=Subquery(sbq),
        branch=F('sale__branch__name')
    ).order_by('-total_sales')[:3]
    for e in employees:
        print(f"{e.name} - {e.total_sales} - {e.branch} - {e.department.name} - {e.district.name}")

