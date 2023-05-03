import decimal

from django.db import models

from basic import managers


class ModelBase(models.Model):
    class Gender(models.TextChoices):
        MALE = ("M", "Male")
        FEMALE = ("F", "Female")

    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, auto_now=True)
    active = models.BooleanField(null=False, default=True)

    class Meta:
        abstract = True


class State(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    abbreviation = models.CharField(max_length=2, null=False)

    class Meta:
        db_table = 'state'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.abbreviation}'


class Zone(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'zone'
        managed = True

    def __str__(self):
        return self.name


class City(ModelBase):
    name = models.CharField(max_length=64, null=False)
    state = models.ForeignKey(
        to='State',
        db_column='id_state',
        on_delete=models.DO_NOTHING,
        null=False
    )

    class Meta:
        db_table = 'city'
        managed = True

    def __str__(self):
        return self.name


class District(ModelBase):
    name = models.CharField(max_length=64, null=False)
    city = models.ForeignKey(
        to='City',
        db_column='id_city',
        on_delete=models.DO_NOTHING,
        null=False
    )
    zone = models.ForeignKey(
        to='Zone',
        db_column='id_zone',
        on_delete=models.DO_NOTHING,
        null=False
    )

    class Meta:
        db_table = 'district'
        managed = True

    def __str__(self):
        return f'{self.name} - {self.city}'


class Branch(ModelBase):
    name = models.CharField(max_length=64, null=False)
    district = models.ForeignKey(
        to='District',
        db_column='id_district',
        on_delete=models.DO_NOTHING,
        null=False
    )

    class Meta:
        db_table = 'branch'
        managed = True

    def __str__(self):
        return f'{self.name}'


class MaritalStatus(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'marital_status'
        managed = True

    def __str__(self):
        return self.name


class Supplier(ModelBase):
    name = models.CharField(max_length=64, null=False)
    legal_document = models.CharField(max_length=20, null=False, unique=True)

    class Meta:
        db_table = 'supplier'
        managed = True


class ProductGroup(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)
    commission_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=False)
    gain_percentage = models.DecimalField(max_digits=6, decimal_places=2, null=False)

    class Meta:
        db_table = 'product_group'
        managed = True


class Product(ModelBase):
    name = models.CharField(max_length=64, null=False)
    cost_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    product_group = models.ForeignKey(
        to="ProductGroup",
        db_column="id_product_group",
        on_delete=models.DO_NOTHING,
        null=False
    )
    supplier = models.ForeignKey(
        to="Supplier",
        db_column="id_supplier",
        on_delete=models.DO_NOTHING,
        null=False
    )

    class Meta:
        db_table = 'product'
        managed = True


class Department(ModelBase):
    name = models.CharField(max_length=64, null=False, unique=True)

    class Meta:
        db_table = 'department'
        managed = True

    def __str__(self):
        return self.name


class Employee(ModelBase):

    name = models.CharField(max_length=64, null=False)
    salary = models.DecimalField(max_digits=16, decimal_places=2, null=False)
    admission_date = models.DateField(null=False)
    birth_date = models.DateField(null=False)
    gender = models.CharField(max_length=1, null=False, choices=ModelBase.Gender.choices)
    department = models.ForeignKey(
        to="Department",
        db_column="id_department",
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="employees"
    )
    district = models.ForeignKey(
        to="District",
        db_column="id_district",
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="employees"
    )
    marital_status = models.ForeignKey(
        to="MaritalStatus",
        db_column="id_marital_status",
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="employees"
    )

    class Meta:
        db_table = 'employee'
        managed = True
        verbose_name = 'Funcionário'
        verbose_name_plural = 'Funcionários'

    def __str__(self):
        return self.name

    def adjustment_salary(self, percentage):
        self.salary += self.salary * (decimal.Decimal(percentage) / 100)


class Customer(ModelBase):
    name = models.CharField(max_length=64, null=False)
    income = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    gender = models.CharField(max_length=1, null=False, choices=ModelBase.Gender.choices)
    district = models.ForeignKey(
        to="District",
        db_column="id_district",
        on_delete=models.DO_NOTHING,
        null=False
    )
    marital_status = models.ForeignKey(
        to="MaritalStatus",
        db_column="id_marital_status",
        on_delete=models.DO_NOTHING,
        null=False
    )

    class Meta:
        db_table = "customer"
        managed = True


class Sale(ModelBase):
    date = models.DateTimeField(null=False)
    customer = models.ForeignKey(
        to="Customer",
        db_column="id_customer",
        on_delete=models.DO_NOTHING,
        null=False
    )
    branch = models.ForeignKey(
        to="Branch",
        db_column="id_branch",
        on_delete=models.DO_NOTHING,
        null=False
    )
    employee = models.ForeignKey(
        to="Employee",
        db_column="id_employee",
        on_delete=models.DO_NOTHING,
        null=False
    )
    objects = managers.SaleManager()

    class Meta:
        db_table = "sale"
        managed = True


class SaleItem(ModelBase):
    quantity = models.DecimalField(max_digits=16, decimal_places=3, null=False)
    sale_price = models.DecimalField(max_digits=16, decimal_places=2, null=False, default=0)
    sale = models.ForeignKey(
        to="Sale",
        db_column="id_sale",
        on_delete=models.DO_NOTHING,
        null=False
    )
    product = models.ForeignKey(
        to="Product",
        db_column="id_product",
        on_delete=models.DO_NOTHING,
        null=False,
        related_name="saleitems"
    )

    class Meta:
        db_table = "sale_item"
        managed = True

