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


class BranchManage(Manager):
    def sold_most(self):
        from basic import models
        from django.db.models import OuterRef, Count, Subquery

        sbq = models.Sale.objects.filter(branch=OuterRef('id')).values('branch_id').annotate(
            total=Count('saleitem__id')
        ).values('total')
        return self.get_queryset().annotate(
            total=Subquery(sbq)
        ).order_by('-total').first()