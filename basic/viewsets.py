from rest_framework import viewsets
from rest_framework.decorators import action
from django.db.models import ExpressionWrapper, F, Value, FloatField, Sum
from rest_framework.response import Response
from basic import models, serializers, filters


class ZoneModelViewSet(viewsets.ModelViewSet):
    queryset = models.Zone.objects.all()
    serializer_class = serializers.ZoneSerializer
    filterset_class = filters.ZoneFilter
    ordering = ('-id',)
    ordering_fields = '__all__'


class MaritalStatusModelViewSet(viewsets.ModelViewSet):
    queryset = models.MaritalStatus.objects.all()
    serializer_class = serializers.MaritalStatusSerializer


class StateModelViewSet(viewsets.ModelViewSet):
    queryset = models.State.objects.all()
    serializer_class = serializers.StateSerializer


class DepartmentModelViewSet(viewsets.ModelViewSet):
    queryset = models.Department.objects.all()
    serializer_class = serializers.DepartmentSerializer


class SupplierModelViewSet(viewsets.ModelViewSet):
    queryset = models.Supplier.objects.all()
    serializer_class = serializers.SupplierSerializer
    
    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.prefetch_related('product_set')
        return super(SupplierModelViewSet, self).list(request, *args, **kwargs)


class ProductGroupModelViewSet(viewsets.ModelViewSet):
    queryset = models.ProductGroup.objects.all()
    serializer_class = serializers.ProductGroupSerializer


class EmployeeModelViewSet(viewsets.ModelViewSet):
    queryset = models.Employee.objects.select_related('supplier', 'product_group').all()
    serializer_class = serializers.EmployeeSerializer
    filterset_class = filters.EmployeeFilter

    @action(methods=['PATCH'], detail=True)
    def adds_percentage_increase_salary(self, request, *args, **kwargs):
        employee = self.get_object()
        percentage = request.data.get('percentage')

        employee.adjustment_salary(percentage)
        employee.save()
        result = self.get_serializer(instance=employee, context=self.get_serializer_context())
        return Response(data=result.data, status=200)


class SaleModelViewSet(viewsets.ModelViewSet):
    queryset = models.Sale.objects.all()
    serializer_class = serializers.SaleSerializer

    @action(methods=['GET'], detail=False)
    def total_per_year(self, request, *args, **kwargs):
        queryset = models.Sale.objects.total_per_year()
        result = serializers.SaleTotalPerYearSerializer(
            instance=queryset, many=True, context=self.get_serializer_context()
        )
        return Response(data=result.data, status=200)


class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.select_related('supplier').all()
    serializer_class = serializers.ProductSerializer
    filterset_class = filters.ProductFilter

