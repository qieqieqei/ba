from django.shortcuts import render,redirect
from goods.models import GoodsInfo
from .models import OrderInfo,OrderGoods
from django.shortcuts import render
import time



def index(request):
    goods = GoodsInfo.objects.all()  # 获取所有商品数据
    return render(request, 'index.html', {'goods': goods})
def add_cart(request):
    """添加商品到购物车"""
    # 获取传过来的商品id
    goods_id = request.GET.get('id', '')
    if goods_id:
        # 获得上一页面地址
        prev_url = request.META['HTTP_REFERER']
        response = redirect(prev_url)
        # 把商品id存到cookie里
        # 获取之前商品在购物车的数量
        goods_count = request.COOKIES.get(goods_id, '')
        # 如果之前购物车里有商品，那么就在之前的数量上+1
        # 如果之前没有 那么就添加1个
        if goods_count:
            goods_count = int(goods_count) + 1
        else:
            goods_count = 1
        # 把商品id和数量保存到cookie中
        response.set_cookie(goods_id, goods_count)

    return response


def show_cart(request):
    """展示购物车商品"""
    cart_goods_list = []  # 读取购物车商品列表
    cart_goods_count = 0  # 商品总数
    cart_goods_money = 0  # 商品总价
    for goods_id, goods_num in request.COOKIES.items():
        # 商品ID都为数字, 非数字的cookie过滤掉
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        # 累加购物车商品总数
        cart_goods_count = cart_goods_count + int(goods_num)
        # 累计商品总价
        cart_goods_money += int(goods_num) * cart_goods.goods_price
    return render(request, 'cart.html', {'cart_goods_list': cart_goods_list,
                                         'cart_goods_count': cart_goods_count,
                                         'cart_goods_money': cart_goods_money})


def remove_cart(request):
    """删除购物车商品"""
    goods_id = request.GET.get('id', '')  # 获得要删除的商品ID
    if goods_id:
        prev_url = request.META['HTTP_REFERER']  # 获得上一页面地址
        response = redirect(prev_url)
        goods_count = request.COOKIES.get(goods_id, '')  # 判断商品的数量
        # print(goods_count)
        if goods_count:
            response.delete_cookie(goods_id)
            return response


def place_order(request):
    """提交订单页面"""
    # 显示购物车中的数据
    cart_goods_list = []  # 读取购物车商品列表
    cart_goods_count = 0  # 商品总数
    cart_goods_money = 0  # 商品总价
    for goods_id, goods_num in request.COOKIES.items():
        # 商品id都为数字, 非数字的cookie过滤掉
        if not goods_id.isdigit():
            continue
        cart_goods = GoodsInfo.objects.get(id=goods_id)
        cart_goods.goods_num = goods_num
        cart_goods.total_money = int(goods_num) * cart_goods.goods_price
        cart_goods_list.append(cart_goods)
        # 累加购物车商品总数
        cart_goods_count = cart_goods_count + int(goods_num)
        # 累计商品总价
        cart_goods_money += int(goods_num) * cart_goods.goods_price
    return render(request, 'place_order.html',
                  {'cart_goods_list': cart_goods_list,
                   'cart_goods_count': cart_goods_count,
                   'cart_goods_money': cart_goods_money})


def submit_order(request):
    """保存订单"""
    # 获得订单信息
    addr = request.POST.get('addr', '')
    recv = request.POST.get('recv', '')
    tele = request.POST.get('tele', '')
    extra = request.POST.get('extra', '')
    # 保存订单信息
    order_info = OrderInfo()
    order_info.order_addr = addr
    order_info.order_tele = tele
    order_info.order_recv = recv
    order_info.order_extra = extra
    # 生成订单编号
    order_info.order_id = str(int(time.time() * 1000)) + \
                          str(int(time.process_time() * 1000000))
    order_info.save()
    # 跳转页面
    response = redirect('/cart/submit_success/?id=%s' % order_info.order_id)

    for goods_id_str, goods_num in request.COOKIES.items():
        if goods_id_str == 'csrftoken':
            continue
        try:
            # 将字符串类型的 goods_id 转换为整数
            goods_id = int(goods_id_str)
        except ValueError:
            # 如果转换失败，记录错误并跳过当前循环
            print(f"Invalid goods_id format: {goods_id_str}")
            continue

        try:
            # 查询商品信息
            cart_goods = GoodsInfo.objects.get(id=goods_id)
            # 创建订单商品信息
            order_goods = OrderGoods()
            order_goods.goods_info = cart_goods
            order_goods.goods_order = order_info
            order_goods.goods_num = int(goods_num)  # 确保 goods_num 也是整数
            order_goods.save()
            # 删除购物车信息
            response.delete_cookie(goods_id_str)
        except GoodsInfo.DoesNotExist:
            # 如果商品不存在，记录错误
            print(f"Goods with ID {goods_id} does not exist.")

    return response


def submit_success(request):
    """显示订单结果"""
    order_id = request.GET.get('id')
    # print(order_id)
    order_info = OrderInfo.objects.get(order_id=order_id)
    # print(order_info)

    order_goods_list = OrderGoods.objects.filter(goods_order=order_info)
    total_money = 0  # 商品总价
    total_num = 0  # 商品总数量
    for goods in order_goods_list:
        goods.total_money = goods.goods_num * goods.goods_info.goods_price
        total_money += goods.total_money
        total_num += goods.goods_num
    return render(request, 'success.html', {'order_info': order_info,
                                            'order_goods_list': order_goods_list,
                                            'total_money': total_money,
                                            'total_num': total_num})
