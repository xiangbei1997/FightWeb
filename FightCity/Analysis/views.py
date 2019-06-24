from django.shortcuts import render
from django.http import HttpResponse, response
import pandas as pd
import json
import re
import sys
import redis
import numpy as np

pool = redis.ConnectionPool(host='106.12.112.207', password='tongna888')
r = redis.Redis(connection_pool=pool)

area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'area.csv')
record_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company_record.csv')
companyAll_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_companyAll.csv')
area = pd.read_csv(area_file, low_memory=False)
record = pd.read_csv(record_file, low_memory=False)
company = pd.read_csv(companyAll_file, low_memory=False)
company = company.set_index('id', drop=False)
record = record.set_index('id', drop=False)
area = area.set_index('id')
area = area.drop(['addDate', 'ids'], axis=1)
area = area.drop(1, axis=0)


# Company_line = []
# for p, d in area['name'].to_dict().items():
#     d = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', d)
#     Company_line.append([{'name': str(d), 'value': 1}])
#     area.loc[p, 'name'] = d


# Create your views here.


# 资金分析数据
def CapitalData(request):
    area_file = '%s\static\Analisis_static\data_csv\c%s\%s' % (sys.path[1], 'apital_csv', 'area.csv')
    company_file = '%s\static\Analisis_static\data_csv\c%s\%s' % (sys.path[1], 'apital_csv', 'xx.csv')
    area = pd.read_csv(area_file)

    data = pd.read_csv(company_file, parse_dates=['addDate', 'lastDate', 'sourceData',
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
        name = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', province_name)
        company_all = data[data['area_id'] == index]['money'].count()
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
    print(xxx['province'])
    return HttpResponse(json.dumps(xxx))


# 资金页面
def CapitalExhibition(request):
    return render(request, 'analysis_templates/AllConstructionCompany.html')


# 资质页面
def Seniority(request):
    pass


# 资质页面
def SeniorityData(request):
    pass


# 备案页面
def RecordPage(request):
    return render(request, 'analysis_templates/Record.html')


# 备案数据
def RecordData(request):
    if request.method == 'POST':
        Company_name = request.POST.get('CompanyName')
        dataType = request.POST.get('type')
        if Company_name:
            companyInfo = company[company['name'] == Company_name]
            companydict = companyInfo.to_dict(orient='records')
            RegistrationArea = companydict[0]['area_id']
            CompanyID = companydict[0]['id']
            nowProvince = area.loc[RegistrationArea]['name']
            ToProvinceRegistration = record[record['company_id'] == CompanyID].groupby('company_id')['area_id']
            Company_line = []
            for p, d in area['name'].to_dict().items():
                d = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', d)
                Company_line.append([{'name': str(d), 'value': 1}])
                area.loc[p, 'name'] = d
            for index, data in ToProvinceRegistration:
                companydict[0]['areaNumber'] = len(data)
                for a in list(data):
                    provinceName = area.loc[a]['name']
                    Company_line.append([{'name': nowProvince, 'value': str(len(data))}, {'name': str(provinceName)}])

            Cdata = {'line': Company_line, 'companyinfo': companydict[0]}
            return HttpResponse(json.dumps(Cdata))
        if int(dataType):
            ProvinceData = r.mget('ProvinceIntoRecord')
            data = json.loads(ProvinceData[0])
            data['type'] = '各省企业到外省备案top10'
            return HttpResponse(json.dumps(data))
    CertProportion = r.mget('recordAll')
    CertProportion = json.loads(CertProportion[0])
    CertProportion['type'] = '省份存在备案企业top10'
    return HttpResponse(json.dumps(CertProportion))


def Record2(request):
    return render(request, 'analysis_templates/Record2.html')


def Search(request):
    return render(request, 'analysis_templates/Search.html')


def vagueSearch(request):
    companyName = request.POST.get('name')
    if companyName:
        name = list(company.loc[company['name'].str.contains(companyName)]['name'].values)
        if name:
            name = name[:10]
            return HttpResponse(json.dumps(name))
    return HttpResponse(json.dumps({'name': '中北交通建设集团有限公司'}))
