# Generated by Django 3.0.8 on 2020-07-24 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0016_auto_20200724_1432'),
        ('orders', '0005_auto_20200724_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_items',
            field=models.ManyToManyField(to='catalog.CartItem'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]