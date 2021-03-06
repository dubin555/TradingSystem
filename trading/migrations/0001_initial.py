# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-31 06:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('symbol', models.CharField(max_length=10)),
                ('type', models.CharField(max_length=12)),
                ('amount', models.IntegerField()),
                ('done_amount', models.IntegerField(default=0, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
                ('valid', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderId',
            fields=[
                ('order_id', models.BigIntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stock',
            fields=[
                ('symbol', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('open_price', models.DecimalField(decimal_places=2, max_digits=8)),
            ],
        ),
        migrations.CreateModel(
            name='StockOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=12)),
                ('amount', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=8, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='APPLE',
            fields=[
                ('stockorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trading.StockOrder')),
            ],
            bases=('trading.stockorder',),
        ),
        migrations.CreateModel(
            name='IBM',
            fields=[
                ('stockorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trading.StockOrder')),
            ],
            bases=('trading.stockorder',),
        ),
        migrations.CreateModel(
            name='WSCN',
            fields=[
                ('stockorder_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='trading.StockOrder')),
            ],
            bases=('trading.stockorder',),
        ),
        migrations.AddField(
            model_name='stockorder',
            name='order_item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trading.Order'),
        ),
    ]
