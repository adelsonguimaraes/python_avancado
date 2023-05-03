from basic import models
from django.db.models import Q, F, ExpressionWrapper, Func, Value, FloatField, Case, When, DurationField, DateField, IntegerField, CharField, Sum, Count
from django.db.models.functions import Now, Cast, ExtractDay, LPad, Replace


# Atividade 1: Fazer uma consulta para retornar todos os funcionários
# que contenham Silva no nome
def all_employees_with_name_silva():
    employees = models.Employee.objects.filter(name__icontains='Silva')
    for e in employees:
        print(e.name)


# Atividade 2: Fazer uma consulta para retornar todos os funcionários
# com salário maior que 5.000
def all_employees_with_salary_greater_5000():
    employees = models.Employee.objects.filter(salary__gt=5000).order_by('salary')
    for e in employees:
        print(f"{e.name} - {e.salary}")


# Atividade 3: Fazer uma consulta para trazer todos os clientes
# que tenham uma renda inferior a 2.000
def all_customers_with_income_less_2000():
    customers = models.Customer.objects.filter(income__lt=2000).order_by('-income')
    for c in customers:
        print(f"{c.name} = {c.income}")


# Atividade 4: Fazer uma consulta para retornar todos os funcionários
# admitidos entre 2010 e 2021
def all_employees_admitted_between_2010_2021():
    employees = models.Employee.objects\
        .filter(admission_date__year__gte='2010', admission_date__year__lte='2021')\
        .order_by('admission_date')
    for e in employees:
        print(f"{e.name} - {e.admission_date}")


# Atividade 5: Nome do funcionário, salário atual + 10%
def all_employees_name_and_salary_plus_ten_percent():
    employees = models.Employee.objects\
        .annotate(new_salary=ExpressionWrapper(F('salary') + (F('salary') * Value(0.10)), output_field=FloatField()))\
        .values('name', 'salary', 'new_salary')

    print(employees)


# Atividade 6: Utilizando case para retornar o sexo
def get_employees_gender():
    return models.Employee.objects.annotate(
        gender_description=Case(
            When(gender=models.ModelBase.Gender.MALE, then=Value('Masculino')),
            default=(Value('Feminino'))
        )
    )


# Atividade 7: Consulta para retornar o nome e um status do funcionário de acordo com seu salário
# até 2000 (vendedor Jr), maior que 2000 e menor ou igual a 5000 (vendedor Pleno),
# acima de 5000 (Vendedor Sênior)
def all_employees_and_status_salary():
    return models.Employee.objects.annotate(
        status_salary=Case(
            When(salary__lte=2000, then=Value("Vendedor Jr")),
            When(Q(salary__gt=2000) & Q(salary__lte=5000), then=Value("Vendedor Pleno")),
            default=Value("Vendedor Sênior")
        )
    ).values('name', 'salary', 'status_salary').order_by('salary')


# Atividade 8: Consulta para retornar distrito, cidade e estado do funcionário, renomeando os campos
def all_employees_district_state_city():
    return models.Employee.objects.annotate(
        bairro=F('district__name'),
        cidade=F('district__city__name'),
        estado=F('district__city__state__name')
    ).values('name', 'bairro', 'cidade', 'estado')


# Atividade 9: Consulta para retornar produto, preço de venda, quantidade, subtotal, valor da comissão
def all_products_with_price_quantity_subtotal_commission(quantity):
    return models.Product.objects.annotate(
        subtotal=ExpressionWrapper(F('sale_price') * quantity, output_field=FloatField()),
        commission=ExpressionWrapper(
            F('subtotal') * F('product_group__commission_percentage') / 100, output_field=FloatField()
        )
    ).values('name', 'sale_price', 'subtotal', 'product_group__commission_percentage', 'commission')


# Atividade 10: Faça uma consulta para retornar todos os funcionários casados ou solteiros
def all_employees_married_or_single():
    employees = models.Employee.objects.filter(
        Q(marital_status__name__exact='Casado') | Q(marital_status__name__exact='Solteiro')
    ).values('name', 'marital_status__name')
    for e in employees:
        print(f"{e['name']} - {e['marital_status__name']}")


# Atividade 11: Faça uma consulta para retornar todos os funcionários que ganham entre R$ 1.000,00 e R$ 5.000,00
def all_employees_earn_between_1000_and_5000():
    employees = models.Employee.objects.filter(
        salary__range=[1000, 5000]
    ).values('name', 'salary').order_by('salary')
    for e in employees:
        print(f"{e['name']} - {e['salary']}")


# Atividade 12: Faça uma consulta que retorne a diferença do preço de custo e do preço de venda dos produtos
def all_products_with_diff_price_cost_and_price_sale():
    products = models.Product.objects.annotate(
        diff_price=ExpressionWrapper(F('sale_price') - F('cost_price'), output_field=FloatField())
    ).values('name', 'cost_price', 'sale_price', 'diff_price')
    for p in products:
        print(f"{p['name']} - {p['cost_price']} - {p['sale_price']} - {p['diff_price']}")


# Atividade 13: Faça uma consulta para retornar todos os funcionários que não tenham salário entre R$ 4.000,00 e R$ 8.000,00
def all_employees_not_earn_between_4000_8000():
    employees = models.Employee.objects.exclude(salary__range=[4000, 8000]).order_by('salary').values('name', 'salary')
    for e in employees:
        print(f"{e['name']} - {e['salary']}")


# Atividade 14: Faça uma consulta para retornar todas as vendas entre 2010 e 2021
def all_sales_between_2010_2021():
    sales = models.Sale.objects.filter(
        date__year__gte=2010, date__year__lte=2021
    ).values('date', 'saleitem__product__name').order_by('date')
    for s in sales:
        print(f"{s['date']} - {s['saleitem__product__name']}")


# Atividade 15: Faça uma consulta que retorne o tipo de funcionário de acordo com a sua idade
def all_employees_with_type_by_age():
    employees = models.Employee.objects.annotate(
        diff=ExpressionWrapper(Cast(Now(), output_field=DateField()) - F('birth_date'), output_field=DurationField()),
        age=ExpressionWrapper(ExtractDay(F('diff')) / 365, output_field=IntegerField()),
        type=Case(
            When(age__range=(18, 25), then=Value('Jr')),
            When(age__range=(26, 35), then=Value('Pl')),
            When(age__gte=36, then=Value('Sr')),
            default=Value('Menor Aprendiz')
        )
    ).values('name', 'age', 'type').order_by('age')
    for e in employees:
        print(f"{e['name']} - {e['age']} - {e['type']}")


# Atividade 16: Fazer uma consulta para retornar um status par o funcionário de acordo com o tempo de casa
def all_employees_status_based_admission_time():
    employees = models.Employee.objects.annotate(
        diff=ExpressionWrapper(
            Cast(Now(), output_field=DateField()) - F('admission_date'), output_field=DurationField()
        ),
        admission_time=ExpressionWrapper(ExtractDay(F('diff')) / 365, output_field=IntegerField()),
        status=Case(
            When(admission_time__lte=2, then=Value('Novato')),
            When(admission_time__range=(3, 5), then=Value('Intermediário')),
            default=Value('Veterano')
        )
    ).order_by('admission_time')
    for e in employees:
        print(f"{e.name} - {e.admission_date} - {e.admission_time} - {e.status}")


# Atividade 17: Uso da função LPAD
def example_lpad():
    return models.Employee.objects.annotate(
        code=LPad(Cast(F('id'), output_field=CharField()), 5, Value('0'))
    ).values('code', 'id', 'name')


# Atividade 18: Retornar a soma de salários por departamento
def total_salary_per_departament():
    employees = models.Employee.objects.select_related('department').values(
        'department__name', 'gender'
    ).annotate(
        sum=Sum('salary')
    ).values('department__name', 'gender', 'sum').order_by('department__name')

    for e in employees:
        print(f"department: {e['department__name']} - gender: {e['gender']} - total: {e['sum']}")


# Atividade 19: Fazer uma consulta para retornar o nome do funcionário e o bairro onde ele mora
def employees_name_and_district():
    employess = models.Employee.objects.select_related('district').values('name', 'district__name')
    for e in employess:
        print(f"name: {e['name']} - district: {e['district__name']}")


# Atividade 20: Fazer uma consulta para retornar o nome do cliente, cidade e zona que o mesmo mora
def customer_name_city_state_zone():
    customers = models.Customer.objects.select_related('district').values('name', 'district__city__name', 'district__zone__name')
    for c in customers:
        print(f"name: {c['name']} - city: {c['district__city__name']} - zone: {c['district__zone__name']}")


# Atividade 21: Fazer uma consulta para retornar filial, estado e cidade onde a mesma está localizada
def branch_state_city():
    branchs = models.Branch.objects.select_related('district').values('name', 'district__city__state__name', 'district__city__name')
    for b in branchs:
        print(f"name: {b['name']} - state: {b['district__city__state__name']} - city: {b['district__city__name']}")


# Atividade 22: Fazer uma consulta para retornar dados do funcionário,
# departamento onde ele trabalha e qual seu estado civil atual
def employee_department_marital_status():
    employees = models.Employee.objects.select_related('department', 'marital_status').values(
        'name', 'department__name', 'marital_status__name'
    )
    for e in employees:
        print(f"name: {e['name']} - department: {e['department__name']} - marital_status: {e['marital_status__name']}")


# Atividade 23: Fazer uma consulta para retornar o nome do produto vendido, o preço unitário e o subtotal
def product_price_subtotal():
    products = models.SaleItem.objects.prefetch_related('product').annotate(
        subtotal=ExpressionWrapper((F('product__sale_price') * F('quantity')), output_field=FloatField())
    ).values('product__name', 'product__sale_price', 'subtotal').order_by('product__name')
    for p in products:
        print(f"product: {p['product__name']} - sale_price: {p['product__sale_price']} - subtotal: {p['subtotal']}")


# Atividade 24: Fazer uma consulta para retornar o nome do produto,
# subtotal e quanto deve ser pago de comissão por cada item
def product_subtotal_commission():
    products = models.SaleItem.objects.annotate(
        subtotal=ExpressionWrapper(F('product__sale_price') * F('quantity'), output_field=FloatField()),
        commission=ExpressionWrapper(
            F('product__product_group__commission_percentage') * F('product__sale_price') / 100,
            output_field=FloatField()
        )
    ).values('product__name', 'subtotal', 'commission')
    for p in products:
        print(f"product: {p['product__name']} - subtotal: {p['subtotal']} - commission: {p['commission']}")


# Atividade 25: Fazer uma consulta para retornar o nome do produto, subtotal e quanto foi obtido de lucro por item
def product_gain():
    products = models.SaleItem.objects.annotate(
        subtotal=ExpressionWrapper(F('product__sale_price') * F('quantity'), output_field=FloatField()),
        gain=ExpressionWrapper(
            F('product__product_group__gain_percentage') * F('product__sale_price') / 100,
            output_field=FloatField()
        )
    ).values('product__name', 'subtotal', 'gain')
    for p in products:
        print(f"product: {p['product__name']} - subtotal: {p['subtotal']} - gain: {p['gain']}")


# Atividade 26: Ranking dos 10 funcionários mais bem pagos
def highest_paid_employee():
    employees = models.Employee.objects.values('name', 'salary').order_by('-salary')[:10]
    for e in employees:
        print(f"{e['name']} - {e['salary']}")


# Ativiade 27: Ranking dos 20 clientes que tem a menor renda mensal
def customers_with_lower_monthly_income():
    customers = models.Customer.objects.values('name', 'income').order_by('income')[:20]
    for c in customers:
        print(f"{c['name']} - {c['income']}")


# Atividade 28: Trazer do décimo primeiro ao vigésimo funcionário mais bem pago
def highest_paid_10_to_21_employee():
    employees = models.Employee.objects.values('id', 'name', 'salary').order_by('-salary')[10:21]
    for e in employees:
        print(f"{e['id']} - {e['name']} - {e['salary']}")


# Atividade 29: Ranking dos produtos mais caros vendidos no ano de 2021
def ranking_products_large_sales_in_2021():
    products = models.SaleItem.objects.select_related('product', 'sale').filter(sale__date__year__exact=2021)\
        .values('product__name', 'product__sale_price', 'sale__date')\
        .order_by('-product__sale_price')
    for p in products:
        print(f"{p['product__name']} - {p['product__sale_price']} - {p['sale__date']}")


# Atividade 30: Criar uma consulta para trazer o primeiro nome dos funcionários.
# Remover se tiver (Sr. Sra Dr. Dra.)
def employee_first_name_remove_prefixes():
    employees = models.Employee.objects.annotate(
        first_name=Case(
            When(name__icontains='Sr.', then=Replace(F('name'), Value('Sr. '), Value(''))),
            When(name__icontains='Sra.', then=Replace(F('name'), Value('Sra. '), Value(''))),
            When(name__icontains='Dr.', then=Replace(F('name'), Value('Dr. '), Value(''))),
            When(name__icontains='Dra.', then=Replace(F('name'), Value('Dra. '), Value(''))),
            default='name'
        )
    )
    for e in employees:
        print(f"{e.first_name}")


# Atividade 31: Criar uma consulta para trazer o último nome dos clientes.
# def customer_last_name():
#     models.Customer.objects.values()


# Atividade 32: Criar uma consulta para trocar quem tem Silva no nome para Oliveira.
def alter_name_silva_to_oliveira():
    employees = models.Employee.objects.filter(name__icontains='Silva').annotate(
        new_name=Replace(F('name'), Value('Silva'), Value('Oliveira'))
    ).values('name', 'new_name')
    for e in employees:
        print(f"{e['name']} - {e['new_name']}")


# Atividade 33: Criar uma consulta para trazer o total de funcionário por estado civil
def total_employees_to_marital_status():
    employees = models.Employee.objects.select_related('marital_status').values('marital_status__name').annotate(
        total=Count('id')
    ).values('marital_status__name', 'total')
    for e in employees:
        print(f"{e['marital_status__name']} - {e['total']}")


# Atividade 34: Criar uma consulta para trazer o total vendido em valor R$ por filial
def total_sale_per_branch():
    branches = models.SaleItem.objects.select_related('sale__branch').values('sale__branch').annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        )),
        branch=F('sale__branch__name')
    ).values('branch', 'total')
    for b in branches:
        print(f"{b['branch']} - {b['total']}")


# Atividade 35: Criar uma consulta para trazer o total vendido em valor R$ por zona
def total_sale_per_zone():
    sales = models.SaleItem.objects.select_related('sale').values('sale__branch__district__zone__name').annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        )),
        zone=F('sale__branch__district__zone__name')
    ).values('zone', 'total')
    for s in sales:
        print(f"{s['zone']} - {s['total']}")


# Atividade 36: Criar uma consulta para trazer o total vendido por estado
def total_sale_per_state():
    sales = models.SaleItem.objects.select_related('sale').values('sale__branch__district__city__state__name').annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        )),
        state=F('sale__branch__district__city__state__name')
    ).values('state', 'total')
    for s in sales:
        print(f"{s['state']} - {s['total']}")


# Atividade 37: Criar uma consulta para trazer o total vendido por ano
def total_sale_per_year():
    sales = models.SaleItem.objects.select_related('sale').values('sale__date__year').annotate(
        total=Sum(ExpressionWrapper(
            F('quantity') * F('product__sale_price'), output_field=FloatField()
        )),
        year=F('sale__date__year')
    ).values('year', 'total').order_by('year')
    for s in sales:
        print(f"{s['year']} - {s['total']}")
