import redis
import sys
import pandas as pd
import time
import re
import json
import requests


# pool = redis.ConnectionPool(host='106.12.112.207', password='tongna888')
# r = redis.Redis(connection_pool=pool)
# xx = r.mget('LineCompany')
# print(json.loads(xx[0]))


# def test1():
#     area_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'area.csv')
#     record_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company_record.csv')
#     company_file = '%s\static\Analisis_static\data_csv\%s\%s' % (sys.path[1], 'Record', 'data_company.csv')
#     area = pd.read_csv(area_file, low_memory=False)
#     record = pd.read_csv(record_file, low_memory=False)
#     company = pd.read_csv(company_file, low_memory=False)
#     company = company.set_index('id', drop=False)
#     record = record.set_index('id', drop=False)
#     area = area.set_index('id')
#     area = area.drop(['addDate', 'ids'], axis=1)
#     area = area.drop(1, axis=0)
#     Company_line = []
#     for p, d in area['name'].to_dict().items():
#         d = re.sub('["省"，"壮族自治区", "回族自治区", "市","维吾尔自治区"]', '', d)
#         Company_line.append([{'name': d, 'value': 1}])
#         area.loc[p, 'name'] = d
#     print(company.loc[88783])
#     cc = company.loc[88783]['area_id']
#     nowProvince = area.loc[cc]['name']
#     xx = record[record['company_id'] == 88783].groupby('company_id')['area_id']
#
#     for index, data in xx:
#         for a in list(data):
#             mm = area.loc[a]['name']
#             Company_line.append([{'name': nowProvince, 'value': str(len(data))}, {'name': mm}])
#     data1 = json.dumps(Company_line, ensure_ascii=False)
#
#     nn = r.set('LineCompany', data1)
#     print(nn)


#
# start_time = time.time()
# print('开始时间：%s' % start_time)
# test1()
# end_time = time.time()
# print('结束时间：%s' % end_time)
# print('共用：%s' % (end_time - start_time))


def test3():
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
    print(company.loc[company['name'].str.contains('中北')]['name'].values)


start_time = time.time()
print('开始时间：%s' % start_time)
test3()
end_time = time.time()
print('结束时间：%s' % end_time)
print('共用：%s' % (end_time - start_time))
