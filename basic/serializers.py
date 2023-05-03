from rest_framework import serializers
from basic import models
from rest_flex_fields import FlexFieldsModelSerializer


class ZoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Zone
        fields = '__all__'

    def validate(self, attrs):
        if not attrs.get('name').isupper():
            raise Exception('O nome deve ser uppercase')
        return super(ZoneSerializer, self).validate(attrs)

# class ZoneSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     created_at = serializers.DateTimeField(read_only=True)
#     modified_at = serializers.DateTimeField(read_only=True)
#     active = serializers.BooleanField(required=False)
#     name = serializers.CharField(required=True, max_length=64)
#
#     def validate(self, attrs):
#         return super(ZoneSerializer, self).validate(attrs)
#
#     def create(self, validated_data):
#         return models.Zone.objects.create(**validated_data)
#
#     def update(self, instance, validated_data):
#         for key, value in validated_data.items():
#             setattr(instance, key, value)
#         instance.save()
#         return instance
#
#     def to_representation(self, instance):
#         data = super(ZoneSerializer, self).to_representation(instance)
#         return data


class MaritalStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MaritalStatus
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Department
        fields = '__all__'


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.State
        fields = '__all__'


class ProductSupplierListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'name']


class SupplierSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Supplier
        fields = '__all__'

    expandable_fields = {
        'products': ('basic.ProductSerializer', {'source': 'product_set', 'many': True})
    }


class ProductGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductGroup
        fields = '__all__'


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Employee
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Sale
        fields = '__all__'


class SaleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SaleItem
        fields = '__all__'


class SaleTotalPerYearSerializer(serializers.ModelSerializer):
    year = serializers.IntegerField(read_only=True)
    month = serializers.IntegerField(read_only=True)
    total = serializers.DecimalField(read_only=True, max_digits=16, decimal_places=2)


class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = models.Product
        fields = '__all__'

    expandable_fields = {
        'supplier': ('basic.SupplierSerializer',),
        'product_group': ('basic.ProductGroupSerializer',)
    }
