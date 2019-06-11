from django.shortcuts import render
# from django.http import HttpResponse


# Create your views here.


# 应用首页
def first(request):
    return render(request, 'currency/404.html')
