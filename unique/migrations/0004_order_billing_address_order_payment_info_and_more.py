# Generated by Django 4.2.7 on 2024-10-01 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unique', '0003_basket_order_basketitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='billing_address',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='order',
            name='payment_info',
            field=models.CharField(default='', max_length=150),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_addr',
            field=models.TextField(default=''),
        ),
    ]
