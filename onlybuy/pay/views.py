from django.shortcuts import render
from django.http import HttpResponse
from stdnum import luhn
from .models import *
from order.models import *
import json
import random
import time
from userinfo.views import check_login_status
# Create your views here.


# 绑定银行卡
def addbank(request):
    if request.method == 'POST':
        user = request.user
        bank = request.POST.get("bank", "")
        bankid = request.POST.get("bankid", "")
        status = request.POST.get("status", "")
        if bank and bankid:
            if luhn.is_valid(bankid):
                Bank.objects.create(user=user, bank=bank, bankid=bankid, status=status)
                return HttpResponse(json.dumps({"result": True, "data": "绑定成功", "error": ""}))
            else:
                return HttpResponse(json.dumps({"result": False, "data": "", "error": "无效卡号"}))
        else:
            return HttpResponse(json.dumps({"result":False, "data":"", "error":"输入项不能为空"}))
    if request.method == 'GET':
        return HttpResponse(json.dumps({"result": True, "data": "", "error": ""}))


# 银行列表
def banklist():
    banks = Banklist.objects.all()
    banklst = []
    for bank in banks:
        a = {}
        a["bankid"] = bank.id
        a["bankimg"] = "/images/" + str(bank.bankimg)
        banklst.append(a)
    return banklst


# 支付
@check_login_status
def payorder(request):
    if request.method == "POST":
        user = request.user
        orderNo = request.POST.get("orderNo", "")
        bankid = request.POST.get("bankid", "")
        bankinfo = Banklist.objects.filter(id=bankid)
        bank = bankinfo[0].bank
        time.sleep(3)
        la = random.randint(0,1)
        if la<0.5:
            Order.objects.filter(orderNo=orderNo, user=user).update(status=1, bank=bank)
            return HttpResponse(json.dumps({"result": True, "data": "支付成功", "error": ""}))
        else:
            Order.objects.filter(orderNo=orderNo, user=user).update(status=4, bank=bank)
            return HttpResponse(json.dumps({"result": False, "data": "", "error": "支付失败"}))
