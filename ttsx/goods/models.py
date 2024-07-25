import os
from django.utils.deconstruct import deconstructible
from django.db import models


@deconstructible
class CustomPathAndRename:
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # 获取文件名和扩展名
        base, ext = os.path.splitext(filename)
        # 生成新的文件名，这里使用商品名替代，可以根据需要更改
        new_name = instance.goods_name
        # 返回新的文件路径
        return os.path.join(self.sub_path, new_name + '.jpg')
# 商品分类
# 模型类 对应了数据库中的一张表
class GoodsCategory(models.Model):
    """商品分类模型"""
    # 分类名称  max_length 最大长度，字符串类型必须定义
    cag_name = models.CharField(max_length=30)
    # 分类样式
    cag_css = models.CharField(max_length=20)
    # 分类图片
    cag_img = models.ImageField(upload_to='static/images/')

    def save(self, *args, **kwargs):
        super(GoodsCategory, self).save(*args, **kwargs)
        # 获取文件名和扩展名
        file_name_with_ext = os.path.basename(self.cag_img.name)
        # 更新字段以仅存储 images/ 目录中的文件路径
        self.cag_img.name = os.path.join('images', file_name_with_ext)
        super(GoodsCategory, self).save(update_fields=['cag_img'])


# 商品表
# 模型类
class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=100)
    goods_price = models.IntegerField(default=0)
    goods_desc = models.CharField(max_length=1000)
    goods_img = models.ImageField(upload_to=CustomPathAndRename('static/goods/'))
    goods_cag = models.ForeignKey(GoodsCategory, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(GoodsInfo, self).save(*args, **kwargs)
        # 获取文件名（不包括路径和后缀）
        file_name_without_ext = os.path.splitext(os.path.basename(self.goods_img.name))[0]
        # 更新字段以仅存储文件名（不带后缀）
        self.goods_img.name = file_name_without_ext
        super(GoodsInfo, self).save(update_fields=['goods_img'])

# from goods.models import *
# categories = [('时令水果', 'fruit'), ('海鲜水产', 'seafood'),
#               ('全品肉类', 'meet'), ('美味蛋品', 'egg'),
#               ('新鲜蔬菜', 'vegetables'), ('低温奶制品', 'ice')]
# for index,cag in zip(range(1,7),categories):
#     c = GoodsCategory()
#     c.cag_name = cag[0]
#     c.cag_css = cag[1]
#     c.cag_img = 'images/banner0%d.jpg' % index
#     c.save()
#
# from goods.models import *
# goods = GoodsInfo.objects.all()

