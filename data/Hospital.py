#!/usr/bin/env python

import pandas as pd
from collections import Counter

filename1 = 'DepartmentofTreatment.csv'
filename2 = 'HospitalInfo.csv'

DoT = pd.read_csv(filename1, encoding='utf-8')
HI = pd.read_csv(filename2, encoding='utf-8')
# print(DoT.info())
# print(HI.info())

# 산부, 소아 포함하면 숫자 카운트
# DoT에서 진료코드 11 (소아청소년과), 24 (응급의학과), 53 (소아치과), 82 (한방소아과) 골라내기

# imsi = pd.DataFrame(columns=DoT.columns)
#
# for i, row in DoT.iterrows():
#     if row['진료과목코드'] == 11 or row['진료과목코드'] == 24 or row['진료과목코드'] == 53 or row['진료과목코드'] == 82:
#         imsi = pd.concat([imsi, row.to_frame().T], ignore_index=True)
#
# filename = 'imsi.csv'
# imsi.to_csv(filename, encoding='utf8')
# filename3 = 'imsi.csv'
# imsi = pd.read_csv(filename3, encoding='utf-8')
#
# for i in range (len(imsi)):
#     if imsi['과목별 전문의수'][i] == 0:
#         imsi = imsi.drop(i, axis=0)
#
# filename = 'imsi2.csv'
# imsi.to_csv(filename, encoding='utf-8')
filename4 = 'imsi2.csv'
imsi2 = pd.read_csv(filename4, encoding='utf-8')

imsi2 = imsi2.drop_duplicates(['암호화요양기호'], keep='first')

addr = []
realaddr = []
imsi2 = imsi2.sort_values('암호화요양기호')
HI = HI.sort_values('암호화요양기호')
for code in imsi2['암호화요양기호']:
    mask = HI['암호화요양기호'] == code
    if mask.any():
        address = HI.loc[mask, '주소'].values[0]
        realaddr.append(address)

for i in range (len(realaddr)):
    splitaddr = realaddr[i].split()[:2]
    if splitaddr[0] == '세종특별자치시':
        splitaddr[1] = '세종시'
    addr.append(' '.join(splitaddr))

dfaddr = pd.DataFrame({"행정구역":addr})
dfaddr = dfaddr['행정구역'].value_counts()

filename = 'HosAddr.csv'
dfaddr.to_csv(filename, encoding='utf-8')
print(dfaddr)