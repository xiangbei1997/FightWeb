from django.test import TestCase

# Create your tests here.

import re

# a = '\n\n\n文\xa0\xa0\xa0\xa0字\n\n\n'
# s = re.sub('["省"，"壮族自治区", "回族自治区"]', '', a)
# print(s)

xx = ['山西省', '西藏自治区', '广西壮族自治区', '宁夏回族自治区']
for x in xx:
    s = re.sub('["省"，"壮族自治区", "回族自治区", ]', '', x)
    print(s)

