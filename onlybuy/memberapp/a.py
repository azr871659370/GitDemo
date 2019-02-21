#coding=utf-8
import requests
from bs4 import BeautifulSoup
import json
import urllib
import os
from .models import *

def getPic():
    print("!!!!!!!!!!!!!!!")
    promision = [{'title': '急速退款', 'detail': '3X24小时急速退款'}, {'title': '无理由退货', 'detail': '7天无理由退货服务'}, {'title': '闪电发货', 'detail': '24小时急速发货'}, {'title': '自提', 'detail': '自提享受减免优惠'}, {'title': '99元免运费', 'detail': '所选地址满99元免运费'}, {'title': '可配送海外', 'detail': '支持收货地址为海外'}, {'title': '延长保修', 'detail': '免费增加保修一年'}]
    datas = [{'type': 'lvxingxiang', 'num': [100324,103200,250,103783,100542,103372,102339,102742,102746,102941,102515,102112]},{'type':'beibao','num':[104295,104179,890,103787,103390,462,103360,103206,103212,103216,102552,101814,102747,100655,102744,760,102225,759,101618,655,891]},{'type': 'nvshibaodai','num':[104330,102118,101427,891]},{'type': 'gongnnegxiangbao','num':[101826,102818,102548,102837,102096,103207,103209,103211,103215,103213,102381,712,772,902,100332,100411]},{'type': 'qianbao','num':[603,741,604,101420,605,103208,101443,601,600]}]
    p=[]
    for pr in promision:
        prtitle = pr['title']
        prdetail = pr['detail']
        a = Promise.objects.create(title=prtitle, desc=prdetail)
    for dataa in datas:
        for j in dataa['num']:
            p.append(j)
            print('id',j)
            resp = requests.get('https://youpin.mi.com/detail?gid='+str(j))
            if resp .status_code != 200:
                return
            cookies = resp.cookies.get_dict()
            soup = BeautifulSoup(resp.text,'lxml')
            data = {
                 'data':'{"detail":{"model":"Shopv2","action":"getDetail","parameters":{"gid":"'+str(j)+'"}},"comment":{"model":"Comment","action":"getList","parameters":{"goods_id":"'+str(j)+'","orderby":"1","pageindex":"0","pagesize":3}},"activity":{"model":"Activity","action":"getAct","parameters":{"gid":"'+str(j)+'"}}}'
            }
            res = requests.post('https://youpin.mi.com/app/shop/pipe', data=data,cookies=cookies)
            html = res.text
            name = json.loads(html)['result']['detail']['data']['good']['name']
            price = float(json.loads(html)['result']['detail']['data']['good']['price_min'])/100
            desc = json.loads(html)['result']['detail']['data']['good']['summary']
            if os.path.isdir('./images/goods/'+str(j)):
                pass
            else:
                os.mkdir('./images/goods/'+str(j))
            print(name)
            if dataa['type'] == 'shuangjianbei' or dataa['type'] == 'beibao':
                id = 2
            elif dataa['type'] == 'nvshibaodai' or dataa['type'] == 'qianbao':
                id = 3
            elif dataa['type'] == 'gongnnegxiangbao' or dataa['type'] == 'lvxingxiang':
                id = 1
            type = GoodsType.objects.get(id=id)
            goods = Goods.objects.create(title=name,price=price,desc=desc,listimg='/list/'+str(j)+'.png',isDelete=False,type=type)

            if len(json.loads(html)['result']['detail']['data']['group'])>0:
                if json.loads(html)['result']['detail']['data']['group'][0]['name'] == '颜色':
                    for color in json.loads(html)['result']['detail']['data']['group'][0]['tags']:
                        print(color['name'])
                        GoodsColor.objects.create(color=color['name'],goods=goods)
                else:
                    for size in json.loads(html)['result']['detail']['data']['group'][0]['tags']:
                        print(size['name'])
                        GoodsDetail.objects.create(specifice=size['name'], stock=2, goods=goods)
            else:
                GoodsColor.objects.create(color='主图颜色', goods=goods)

            if len(json.loads(html)['result']['detail']['data']['group'])>1:
                for size in json.loads(html)['result']['detail']['data']['group'][1]['tags']:
                    print(size['name'])
                    GoodsDetail.objects.create(specifice=size['name'],stock=2,goods=goods)
            else:
                GoodsDetail.objects.create(specifice='标准规格', stock=2, goods=goods)
            if len(json.loads(html)['result']['detail']['data']['good']['album'])>0:
                num = 1
                for picurl in json.loads(html)['result']['detail']['data']['good']['album']:
                    picurlb = picurl +'&w=1080&h=1270&w=366&h=431&t=webp'
                    picurl = picurl +'&w=166&h=196&t=webp'
                    picb = requests.get(picurlb)
                    pic = requests.get(picurl)
                    stringb = '/goods/'+str(j)+'/'+str(num + 1) + 'big.jpg'
                    string = '/goods/'+str(j)+'/'+str(num + 1) + '.jpg'
                    if os.path.isdir('./images'+string):
                        pass
                    else:
                        with open('./images'+string, 'wb') as f:
                            f.write(pic.content)
                    if os.path.isdir('./images'+stringb):
                        pass
                    else:
                        with open('./images'+stringb, 'wb') as f:
                            f.write(picb.content)
                    GoodsImg.objects.create(goodsimg=string,goodsimgbig=stringb,goods=goods)
                    num = num+1
                    print(picurl+'&w=1080&h=1270&w=366&h=431&t=webp')
    print(p)
    return 'success'

