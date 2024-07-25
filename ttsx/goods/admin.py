from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import GoodsCategory, GoodsInfo

admin.site.register(GoodsCategory)
admin.site.register(GoodsInfo)
