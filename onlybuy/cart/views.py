from django.shortcuts import render
from .models import *
from memberapp import *
from django.db import DatabaseError
from django.http import request, response, HttpResponse
from userinfo.views import check_login_status
from django.db.models import F
import logging
import json
from django.core import serializers
import decimal
# Create your views here.

# 购物车
@check_login_status
def add_cart(request):
    if request.method == "POST":
        user = request.user
        goodsid = request.POST.get("goodsid", "")
        colorid = request.POST.get("colorid", "")
        sperid = request.POST.get("sperid", "")
        amount = request.POST.get("amount", "")
        try:
            goods = Goods.objects.get(id=goodsid)
            goodcolor = GoodsColor.objects.get(id=colorid)
            goodspe = GoodsDetail.objects.get(id=sperid)
        except DatabaseError as e:
            logging.warnning(e)
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "异常"}))
        allcart = Cart.objects.all()
        if len(allcart) < 120:
            oldcart = Cart.objects.filter(user_id=user.id, goods_id=goodsid, color=goodcolor.color,
                                          spec=goodspe.specifice)
            if oldcart:
                oldcart[0].amount = oldcart[0].amount + int(amount)
                oldcart[0].save()
            else:
                new_cart = Cart()
                new_cart.user = user
                new_cart.goods = goods
                new_cart.color = goodcolor.color
                new_cart.spec = goodspe.specifice
                new_cart.price = decimal.Decimal(goods.price)
                new_cart.amount = int(amount)
                new_cart.save()
            cart = Cart.objects.filter(user=user, goods=goods, color=goodcolor.color,
                                spec=goodspe.specifice)
            cartid = cart[0].id
            return HttpResponse(json.dumps({"result": True, "data": cartid, "error": ""}))
        else:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "购物车数量超过限制"}))
    elif request.method == "GET":
        pass


@check_login_status
def favor_to_cart(request):
    if request.method == "POST":
        user = request.user
        favors = json.loads(request.POST.get("favor", ""))
        clist = []
        favd_id = ""
        for fav in favors:
            fav_id = fav["favid"]
            good_id = fav["goodsid"]
            if favd_id != '':
                favd_id = favd_id + ',' + fav_id
            else:
                favd_id = fav_id
            good = Goods.objects.filter(id=good_id)[0]
            favor = Favorite.objects.filter(id=fav_id)[0]
            cart_good = Cart.objects.filter(goods_id=good_id)
            if cart_good:
                cart_good[0].amount = cart_good[0].amount + 1
                cart_good[0].save()
            else:
                clist.append(Cart(user=user, goods=good, color=favor.color, spec=favor.spec, price=good.price, amount=1))
        Cart.objects.bulk_create(clist)
        Favorite.objects.extra(where=['id IN (' + favd_id + ')']).delete()
        return HttpResponse(json.dumps({"result": True, "data": "添加成功", "error": ""}))


@check_login_status
def delete_cart(request):
    if request.method == "GET":
        user = request.user
        cartid = request.GET.get("cartid", "")
        try:
            Cart.objects.extra(where=['id IN (' + cartid + ')']).delete()
        except DatabaseError as e:
            logging.warning(e)
            return HttpResponse(json.dumps({"result": False, "data": "ID不存在", "error": ""}))
        return HttpResponse(json.dumps({"result": True, "data": "删除成功", "error": ""}))


@check_login_status
def change_cart(request):
    if request.method == "GET":
        user = request.user
        cartid = request.GET.get("cartid", "")
        single = request.GET.get("single", "")
        single = int(single)
        try:
            delcart = Cart.objects.filter(user_id=user.id, id=cartid)
            if single == 0:
                delcart.update(amount=F('amount')+1)
            elif single == 1:
                delcart.update(amount=F('amount')-1)
                if delcart[0].amount <= 0:
                    delcart.delete()
        except BaseException as e:
            logging.warning(e)
        return HttpResponse(json.dumps({"result":"修改成功"}))


@check_login_status
def cart_list(request):
    if request.method == "GET":
        user = request.user
        find_carts = Cart.objects.filter(user_id=user.id)
        find_carts = serializers.serialize("json", find_carts)
        find_carts = Cart.objects.filter(user_id=user.id)
        cart = []
        for find_cart in find_carts:
            cart_good = {}
            cart_good['cartid'] = find_cart.id
            cart_good['goodid'] = find_cart.goods.id
            cart_good['title'] = find_cart.goods.title+" "+find_cart.goods.desc
            cart_good['img'] = str(find_cart.goods.listimg)
            cart_good['color'] = find_cart.color
            cart_good['spec'] = find_cart.spec
            cart_good['price'] = str(find_cart.goods.price)
            cart_good['amount'] = find_cart.amount
            cart.append(cart_good)
        return HttpResponse(json.dumps({"result": True, "data": cart, "error": ""}))


@check_login_status
def add_favorite(request):
    if request.method == "GET":
        user = request.user
        print(user.username)
        goodsid = request.GET.get("goodsid", "")
        colorid = request.GET.get("colorid", "")
        sperid = request.GET.get("sperid", "")
        try:
            goods = Goods.objects.get(id=goodsid)
            goodcolor = GoodsColor.objects.get(id=colorid)
            goodspe = GoodsDetail.objects.get(id=sperid)
        except DatabaseError as e:
            logging.warnning(e)
        favorite = Favorite.objects.filter(user=user, goods_id=goodsid, color=goodcolor.color, spec=goodspe.specifice)
        if favorite:
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "已收藏"}))
        else:
            Favorite.objects.create(user=user, goods=goods, color=goodcolor.color, spec=goodspe.specifice)
            return HttpResponse(json.dumps({"result": True, "data": "添加成功", "error": ""}))


@check_login_status
def delete_favorite(request):
    if request.method == "POST":
        user = request.user
        fids = request.POST.getlist("fids","")
        for fid in fids:
            Favorite.objects.filter(id=fid).delete()
        return HttpResponse(json.dumps({"result": "已取消"}))


# 小图 价格 名
# 收藏
@check_login_status
def list_favorite(request):
    if request.method == 'GET':
        user = request.user
        fa_goods = Favorite.objects.filter(user=user)
        fa_list=[]
        for fgood in fa_goods:
            fa_g = {}
            fa_g['goodsid'] = fgood.goods.id
            fa_g['favid'] = fgood.id
            fa_g['title'] = fgood.goods.title
            fa_g['color'] = fgood.color
            fa_g['spec'] = fgood.spec
            fa_g['price'] = str(fgood.goods.price)
            fa_g['goodsimg'] = str(fgood.goods.listimg)
            fa_list.append(fa_g)
        return HttpResponse(json.dumps({"result": True, "data": fa_list, "error": ""}))


# 立即购买
@check_login_status
def buynow(request):
    if request.method == "POST":
        user = request.user
        goodsid = request.POST.get("goodsid", "")
        colorid = request.POST.get("colorid", "")
        sperid = request.POST.get("sperid", "")
        amount = request.POST.get("amount", "")
        try:
            goods = Goods.objects.get(id=goodsid)
            goodcolor = GoodsColor.objects.get(id=colorid)
            goodspe = GoodsDetail.objects.get(id=sperid)
        except DatabaseError as e:
            logging.warnning(e)
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "异常"}))
        buyit = Buynow()
        buyit.user = user
        buyit.goods = goods
        buyit.color = goodcolor.color
        buyit.spec = goodspe.specifice
        buyit.amount = int(amount)
        buyit.save()
        return HttpResponse(json.dumps({"result": True, "data": "添加成功", "error": ""}))
    elif request.method == "GET":
        pass