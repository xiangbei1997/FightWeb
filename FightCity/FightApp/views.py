from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

# 首页
def home(request):
    if request.method == 'GET':
        test = request.META['REMOTE_ADDR']
        # zz = request.META['HTTP_X_FORWARDED_FOR']
        # print(test, 'IP地址', zz)
        return render(request, 'fight_templates/home.html')


# 订单页面
def order(request):
    if request.method == 'GET':
        return render(request, 'fight_templates/order.html')


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'fight_templates/register.html')
    else:
        # host = request._get_post
        # print(host, 'xxxxxxxxxxxxxx')
        email = request.POST.get('email')
        print(email)
        return HttpResponse(request, 'ok')


