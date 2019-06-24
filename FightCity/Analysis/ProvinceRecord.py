from django.test import TestCase

# Create your tests here.
import pandas as pd
import sys
import re
import json
import time
import redis

pool = redis.ConnectionPool(host='106.12.112.207', password='tongna888')
r = redis.Redis(connection_pool=pool)


def CertProvince():
    area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Seniority', 'area.csv')
    cert_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Seniority', 'data_cert.csv')
    company_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Seniority', 'data_company.csv')
    area = pd.read_csv(area_file)
    cert = pd.read_csv(cert_file)
    company = pd.read_csv(company_file)
    # 资质全部项目存在
    cert_counts = cert.count()

    cert_company = cert.groupby('company_id')['company_id'].count()
    dict_cert = dict(cert_company)
    # 资质最多的的公司
    result_max = max(dict_cert, key=lambda x: dict_cert[x])
    # 资质最少的公司并非一个
    result_min = min(dict_cert, key=lambda x: dict_cert[x])

    every_province_company = company.groupby('area_id')['id']
    province_groupby = every_province_company.unique()
    company_cert_count = every_province_company.count()
    dict_province = dict(province_groupby)
    AllProvince = {}
    for key, value in dict_province.items():
        every_province = area[area['id'] == key]['name']
        province_name = every_province.get_values()[0]
        name = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', province_name)
        AllProvince[name] = {}
        ProvinceAllCert = 0
        WithOutCert = 0
        for v in value:
            try:
                CertCompany = dict_cert[v]
                ProvinceAllCert += CertCompany
            except KeyError:
                WithOutCert += 1
        AllProvince[name]['ProvinceAllCert'] = ProvinceAllCert
        AllProvince[name]['WithOutCert'] = WithOutCert
        AllProvince[name]['ProvinceAll'] = company_cert_count[key]
    print(AllProvince)


def ProvinceReCord():
    area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'area.csv')
    record_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company_record.csv')
    company_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company.csv')
    area = pd.read_csv(area_file, low_memory=False)
    record = pd.read_csv(record_file, low_memory=False)
    company = pd.read_csv(company_file, low_memory=False)
    every_province_company = company.groupby('area_id')['id']
    province_groupby = every_province_company.unique()
    dict_province = dict(province_groupby)
    AllCert = 0
    ACCD = {'data': [], 'total': None}
    for key, value in dict_province.items():
        every_province = area[area['id'] == key]['name']
        province_name = every_province.get_values()[0]
        name = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', province_name)
        AllProvince = {name: {}}
        province_record = 0
        without_record = 0
        total_province_record = 0
        record_area = []
        for v in value:
            xx = record[record['company_id'] == v]
            record_company = xx['area_id'].count()
            if record_company:
                record_company_area = {}
                province_record += 1
                total_province_record += record_company
                record_company_area[v] = list(xx['area_id'].values)
                record_company_area['certNumber'] = int(record_company)
                record_area.append(record_company_area)
            else:
                without_record += 1
        AllProvince[name]['ProvinceRecord'] = int(province_record)
        AllProvince[name]['WithOutRecord'] = int(without_record)
        AllProvince[name]['TotalRecord'] = int(total_province_record)
        AllProvince[name]['RecordNumberArea'] = record_area
        AllCert += total_province_record
        ACCD['data'].append(AllProvince)
        print(AllProvince)
    ACCD['total'] = int(AllCert)

    redis_cert = r.set('CertCompany', str(ACCD))
    print(redis_cert)


def ProvinceIntoRecordCompany():
    area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'area.csv')
    record_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company_record.csv')
    company_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company.csv')
    area = pd.read_csv(area_file, low_memory=False)
    record = pd.read_csv(record_file, low_memory=False)
    company = pd.read_csv(company_file, low_memory=False)
    company = company.set_index('id', drop=False)
    record = record.set_index('id', drop=False)
    area = area.set_index('id')
    area = area.drop(['addDate', 'ids'], axis=1)
    area = area.drop(1, axis=0)
    ProvinceName = area['name'].to_dict()
    ProvinceDict = []
    for key, value in ProvinceName.items():
        number = company[company['area_id'] == key]['id'].count()
        value = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', value)
        ProvinceDict.append(
            {key: value, 'CompanyRecord': [], 'ProvinceRecordNumber': 0, 'ProvinceHaveRecord': 0,
             'CompanyProportion': 0, 'AllRecordProportion': 0,
             'RecordProportion': 0, 'ProvinceCompanyNumber': number,
             'NoRecordCompany': 0
             })
    record_company = record.groupby('company_id')['area_id']
    All = {'RecordAll': 0, 'TotalCompany': len(record_company), 'RecordCompany': 0, 'NoAddress': 0,
           'Province': [], 'One': []}
    print(len(record_company), '长度')

    for index, data in record_company:
        ProvinceID = company.loc[index]['area_id']
        if not pd.isnull(ProvinceID):
            ProvinceID -= 3
            ProvinceDict[int(ProvinceID)]['CompanyRecord'].append({index: list(data), 'Total': len(data)})
            ProvinceDict[int(ProvinceID)]['ProvinceRecordNumber'] += len(data)
            All['RecordAll'] += len(data)
    AllRecordNumber = []
    for index, data in enumerate(ProvinceDict):
        data['ProvinceHaveRecord'] = len(data['CompanyRecord'])
        if data['ProvinceHaveRecord']:
            data['CompanyProportion'] = str(
                (round(data['ProvinceHaveRecord'] / data['ProvinceCompanyNumber'], 4) * 100)) + '%'

            data['AllRecordProportion'] = str(round(data['ProvinceHaveRecord'] / All['TotalCompany'], 4) * 100) + '%'

            All['RecordCompany'] += len(data['CompanyRecord'])

            data['NoRecordCompany'] = data['ProvinceCompanyNumber'] - data['ProvinceHaveRecord']

            CompanySorted = sorted(data['CompanyRecord'], key=lambda company: company['Total'], reverse=True)

            TopFifty = CompanySorted[:49]
            One = CompanySorted[:1]

            if One:
                All['One'].append({'Fierce': One[0], 'ProvinceName': ProvinceDict[index][index + 3]})
            else:
                All['One'].append({'Fierce': {'Total': 0}, 'ProvinceName': ProvinceDict[index][index + 3]})
            All['Province'].append({'name': ProvinceDict[index][index + 3],
                                    'value': [
                                        {'name': '*%s*共有建筑公司家' % ProvinceDict[index][index + 3],
                                         'value': str(data['ProvinceCompanyNumber'])},
                                        {'name': '*%s*共有建筑公司家在外地备案' % ProvinceDict[index][index + 3],
                                         'value': str(data['ProvinceHaveRecord'])},
                                        {'name': '*%s*备案数量' % ProvinceDict[index][index + 3],
                                         'value': str(data['ProvinceRecordNumber'])},
                                        {'name': '*%s*没有在外地备案的公司总数' % ProvinceDict[index][index + 3],
                                         'value': str(data['NoRecordCompany'])},
                                        {'name': '*%s*备案率' % ProvinceDict[index][index + 3],
                                         'value': data['CompanyProportion']},
                                        {'name': '*%s*在全国备案率' % ProvinceDict[index][index + 3],
                                         'value': data['AllRecordProportion']},
                                    ]})
            AllRecordNumber.append({'name': ProvinceDict[index][index + 3], 'value': str(data['ProvinceRecordNumber'])})
    All['NoAddress'] = All['TotalCompany'] - All['RecordCompany']
    All['One'] = sorted(All['One'], key=lambda Fierce: Fierce['Fierce']['Total'], reverse=True)
    data1 = json.dumps(AllRecordNumber, ensure_ascii=False)

    callback1 = r.set('CertNumber', data1)
    print(callback1)


def SummaryRecordInto():
    CertProportion = r.mget('CertData')
    CertProportion = json.loads(CertProportion[0])
    CertNumber = r.mget('CertNumber')
    CertNumber = json.loads(CertNumber[0])
    CertDataAll = {'CertProportion': CertProportion, 'CertNumber': CertNumber, 'LineCompany': []}
    data1 = json.dumps(CertDataAll, ensure_ascii=False)
    all = r.set('recordAll', data1)
    print(all)


def RecordProvince():
    area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'area.csv')
    record_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company_record.csv')
    company_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company.csv')
    area = pd.read_csv(area_file, low_memory=False)
    record = pd.read_csv(record_file, low_memory=False)
    company = pd.read_csv(company_file, low_memory=False)
    company = company.set_index('id', drop=False)
    record = record.set_index('id', drop=False)
    area = area.set_index('id')
    area = area.drop(['addDate', 'ids'], axis=1)
    area = area.drop(1, axis=0)
    ProvinceRecord = record.groupby('area_id')['company_id'].count()
    AllNumber = len(record)
    TopProvince = []
    AllData = []
    for p, d in area['name'].to_dict().items():
        d = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', d)
        area.loc[p, 'name'] = d
        try:
            TopProvince.append({'name': d, 'value': ProvinceRecord.to_dict()[p]})
            ProportionArea = str((round(ProvinceRecord.to_dict()[p] / AllNumber, 4) * 100)) + '%'
            AllData.append({'name': d, 'value': [
                {'name': '外省来备案总数', 'value': ProvinceRecord.to_dict()[p]},
                {'name': '全国备案率', 'value': ProportionArea}]})
        except KeyError:
            TopProvince.append({'name': d, 'value': 0})
            AllData.append({'name': d, 'value': [
                {'name': '外省来备案总数', 'value': 0},
                {'name': '全国备案率', 'value': 0}]})
    CertDataAll = {'CertProportion': AllData, 'CertNumber': TopProvince, 'LineCompany': []}
    data1 = json.dumps(CertDataAll, ensure_ascii=False)
    callback1 = r.set('ProvinceIntoRecord', data1)

    # for key, value in ProvinceRecord:
    #     print(key, value)


start_time = time.time()
print('开始时间：%s' % start_time)
SummaryRecordInto()
end_time = time.time()
print('结束时间：%s' % end_time)
print('共用：%s' % (end_time - start_time))
