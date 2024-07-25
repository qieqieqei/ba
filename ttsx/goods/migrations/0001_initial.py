# Generated by Django 5.0.6 on 2024-06-06 14:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cag_name', models.CharField(max_length=30)),
                ('cag_css', models.CharField(max_length=20)),
                ('cag_img', models.ImageField(upload_to='cag')),
            ],
        ),
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goods_name', models.CharField(max_length=100)),
                ('goods_price', models.IntegerField(default=0)),
                ('goods_desc', models.CharField(max_length=1000)),
                ('goods_img', models.ImageField(upload_to='goods')),
                ('goods_cag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.goodscategory')),
            ],
        ),
    ]
