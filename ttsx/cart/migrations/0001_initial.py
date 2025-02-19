# Generated by Django 5.0.6 on 2024-06-06 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=100)),
                ('order_addr', models.CharField(max_length=100)),
                ('order_recv', models.CharField(max_length=50)),
                ('order_tele', models.CharField(max_length=11)),
                ('order_fee', models.IntegerField(default=10)),
                ('order_extra', models.CharField(max_length=200)),
                ('order_status', models.IntegerField(choices=[(1, '代付款'), (2, '代付款'), (3, '代付款'), (4, '代付款')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='OrderGoods',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_num', models.IntegerField()),
                ('goods_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodsinfo')),
                ('goods_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cart.orderinfo')),
            ],
        ),
    ]
