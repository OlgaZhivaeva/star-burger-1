# Generated by Django 3.2.15 on 2024-10-14 10:36

from django.db import migrations


def add_price(apps, schema_editor):

    OrderItem = apps.get_model('foodcartapp', 'OrderItem')
    items = OrderItem.objects.all().prefetch_related('product')
    for item in items.iterator():
        item.price = item.product.price
        item.save()


class Migration(migrations.Migration):

    dependencies = [
        ('foodcartapp', '0043_orderitem_price'),
    ]

    operations = [
        migrations.RunPython(add_price),
    ]
