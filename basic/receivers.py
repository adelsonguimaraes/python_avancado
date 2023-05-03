from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from basic import models


@receiver(post_save, sender=models.State, dispatch_uid='create_file_state', weak=False)
def create_file_state(instance, **kwargs):
    with open('states.txt', 'a') as file:
        file.write(f'{instance.id}|{instance.name}')


@receiver(pre_save, sender=models.SaleItem, dispatch_uid='save_price_item', weak=False)
def save_price_item(instance, **kwargs):
    instance.sale_price = instance.product.sale_price
