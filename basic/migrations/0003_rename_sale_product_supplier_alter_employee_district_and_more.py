# Generated by Django 4.2 on 2023-05-02 19:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_alter_customer_gender'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='sale',
            new_name='supplier',
        ),
        migrations.AlterField(
            model_name='employee',
            name='district',
            field=models.ForeignKey(db_column='id_district', on_delete=django.db.models.deletion.DO_NOTHING, related_name='employees', to='basic.district'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='marital_status',
            field=models.ForeignKey(db_column='id_marital_status', on_delete=django.db.models.deletion.DO_NOTHING, related_name='employees', to='basic.maritalstatus'),
        ),
        migrations.AlterField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(db_column='id_product', on_delete=django.db.models.deletion.DO_NOTHING, related_name='saleitems', to='basic.product'),
        ),
    ]
