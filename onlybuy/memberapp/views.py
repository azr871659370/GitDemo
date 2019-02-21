from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers
from .a import *
from .models import *

# Create your views here.
def aa(request):
    getPic()
    return HttpResponse('ok')


# id 名 价格 图
# 列表页
def goodlist(request):
    if request.method == 'GET':
        typeid = request.GET.get('typeid')
        if not typeid:
            goods = Goods.objects.all()
            a = []
            for good in goods:
                b = {}
                b['goodid'] = good.id
                b['typeid'] = good.type_id
                b['title'] = good.title
                b['price'] = str(good.price)
                b['goodsimg'] = str(good.listimg)
                a.append(b)
            return HttpResponse(json.dumps({"result": True, "data": a, "error": ""}))
        else:
            goodstype = GoodsType.objects.filter(id=typeid)[0]
            goods = Goods.objects.filter(type_id=goodstype.id)
            a = []
            for good in goods:
                b = {}
                b['goodid'] = good.id
                b['typeid'] = good.type_id
                b['title'] = good.title
                b['price'] = str(good.price)
                b['goodsimg'] = str(good.listimg)
                a.append(b)
            return HttpResponse(json.dumps({"result": True, "data": a, "error": ""}))



# 大图 小图 名 详细描述 价格 规格 颜色

# 详细页
def goodetail(request):
    if request.method == 'GET':
        goodid = request.GET.get('goodid')
        good = Goods.objects.filter(id=goodid).first()
        goodimg = good.goodsimg_set.all()
        gooddetail = good.goodsdetail_set.all()
        goodcolor = good.goodscolor_set.all()
        bigimg = []
        smallimg = []
        for img in goodimg:
            bigimg.append(str(img.goodsimgbig))
            smallimg.append(str(img.goodsimg))
        spelist = []
        for detail in gooddetail:
            spe = {}
            spe["id"] = detail.id
            spe["specifice"] = detail.specifice
            spelist.append(spe)
        colorlist = []
        for gcolor in goodcolor:
            col = {}
            col["id"] = gcolor.id
            col["color"] = gcolor.color
            colorlist.append(col)
        godetail = {}
        godetail['title'] = good.title
        godetail['price'] = str(good.price)
        godetail['desc'] = str(good.desc)
        godetail["promise"] = serializers.serialize("json", good.promise.all())
        godetail['bigimg'] = bigimg
        godetail['smallimg'] = smallimg
        godetail['spelist'] = spelist
        godetail['colorlist'] = colorlist
        return HttpResponse(json.dumps({"result": True, "data": godetail, "error": ""}))


def search(request):
    if request.method == 'GET':
        connect = request.GET.get("connect", "")
        connect = connect.encode('utf-8').decode('unicode_escape')
        goods = Goods.objects.filter(title__contains=connect)
        data = []
        for good in goods:
            a = {}
            a["typeid"] = good.type_id
            a["goodid"] = good.id
            a["title"] = good.title
            a["price"] = str(good.price)
            a["desc"] = good.desc
            # a["promise"] = serializers.serialize("json", good.promise.all())
            a["listimg"] = str(good.listimg)
            data.append(a)
        return HttpResponse(json.dumps({"result": True, "data": data, "error": ""}))


from django.shortcuts import render_to_response
def page_not_found(request):
    return render_to_response('404.html')


