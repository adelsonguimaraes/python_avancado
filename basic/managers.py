from django.db.models import Manager, F, ExpressionWrapper, Sum, FloatField


class SaleManager(Manager):
    def total_per_year(self):
        return self.get_queryset().prefetch_related('saleitem_set')\
            .values('date__year', 'date__month').annotate(
            year=F('date__year'),
            month=F('date__month'),
            total=ExpressionWrapper(Sum(F('saleitem__quantity') * F('saleitem__product__sale_price')),
                                    output_field=FloatField()),
        ).values('month', 'year', 'total').order_by('-date__year', '-date__month')
