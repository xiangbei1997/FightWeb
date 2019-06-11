from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd
import json
import re

# Create your views here.


# 资金分析数据
def CapitalData(request):
    f = 'E:/xx.csv'
    area = pd.read_csv('E:/area.csv')

    data = pd.read_csv(f, parse_dates=['addDate', 'lastDate', 'sourceData',
                                       'validTime', 'regTime', 'startDate',
                                       'endDate', 'updateDate', 'checkDate',
                                       'apprDate',
                                       ])
    data = data.dropna(subset=['money'])
    allc = data['money'].sum()
    cc = data.groupby('area_id')['money'].sum()
    xxx = {'province': [], 'info': []}
    for index, cdata in cc.iteritems():
        every_province = area[area['id'] == index]['name']
        province_name = every_province.get_values()[0]
        company_all = data[data['area_id'] == index]['money'].count()
        name = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', province_name)
        average = cdata / company_all
        cc = {}
        vv = {'name': name, 'value': []}
        province_most_money = data[data['area_id'] == index]['money'].idxmax()
        province_most_less = data[data['area_id'] == index]['money'].idxmin()
        company_info_most = data.loc[[province_most_money, ]]
        company_info_less = data.loc[[province_most_less, ]]
        province_company_capital = str(round((cdata / allc) * 100, 3)) + '%'
        roportion = {'name': '资金占全国百分比', 'value': province_company_capital}

        funds = {'name': '建筑公司资金总和', 'value': cdata}

        company_count = {'name': '建筑公司总和共', 'value': str(company_all)}

        averages = {'name': '公司平均资金', 'value': average}

        most_money_name = {'name': '注册资金最高的公司', 'value': company_info_most['name'].get_values()[0]}
        most_money_number = {'name': '注册资金最高的统一社会信用码', 'value': company_info_most['licenseNum'].get_values()[0]}
        most_money_address = {'name': '注册资金最高的公司地址', 'value': company_info_most['address'].get_values()[0]}
        most_money_money = {'name': '注册资金最高的公司资金', 'value': company_info_most['money'].get_values()[0]}

        less_money_name = {'name': '注册资金最低的公司', 'value': company_info_less['name'].get_values()[0]}
        less_money_number = {'name': '注册资金最低的统一社会信用码', 'value': company_info_less['licenseNum'].get_values()[0]}
        less_money_address = {'name': '注册资金最低的公司地址', 'value': company_info_less['address'].get_values()[0]}
        less_money_money = {'name': '注册资金最低的公司资金', 'value': company_info_less['money'].get_values()[0]}
        province_company = [company_count, roportion, funds, averages, most_money_name, most_money_number,
                            most_money_address,
                            most_money_money, less_money_name, less_money_number, less_money_address, less_money_money,
                            ]
        vv['value'] = province_company
        cc['value'] = int(company_all)
        cc['name'] = str(name)
        xxx['province'].append(cc)
        xxx['info'].append(vv)
    return HttpResponse(json.dumps(xxx))


# 资金页面
def CapitalExhibition(request):
    return render(request, 'fight_templates/AllConstructionCompany.html')
