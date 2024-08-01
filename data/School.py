#!/usr/bin/env python

import pandas as pd

filename1 = 'School.csv'
filename2 = 'Kindergarten.csv'

sc = pd.read_csv(filename1, encoding='utf-8')
kd = pd.read_csv(filename2, encoding='utf-8')
print('head() 메서드 결과')
print(sc.head())
print(kd.head())


for i in range (len(sc)):
    if sc.loc[i, '학교급구분'] != '초등학교':
        sc = sc.drop(i, inplace=False)

filename = 'imsi.csv'
sc.to_csv(filename, encoding='utf8', index=False)
filename3 = 'imsi.csv'
sc = pd.read_csv(filename3, encoding='utf-8')

scaddr = []
screaladdr = []
for i in range (len(sc)):
    screaladdr.append(sc.loc[i, '소재지지번주소'])
for i in range (len(sc)):
    splitaddr = screaladdr[i].split()[:2]
    if splitaddr[0] == '세종특별자치시':
        splitaddr[1] = '세종시'
    elif splitaddr[0] == '전북특별자치도':
        splitaddr[0] = '전라북도'
    scaddr.append(' '.join(splitaddr))

dfaddrsc = pd.DataFrame({'행정구역':scaddr})
dfaddrsc = dfaddrsc['행정구역'].value_counts()

kdaddr = []
kdrealaddr = []
for i in range (len(kd)):
    kdrealaddr.append(kd.loc[i, '주소'])
for i in range (len(kd)):
    splitaddr = kdrealaddr[i].split()[:2]
    if splitaddr[0] == '세종특별자치시':
        splitaddr[1] = '세종시'
    elif splitaddr[1] == '군위군':
        splitaddr[0] = '대구광역시'
    elif splitaddr[0] == '경기':
        splitaddr[0] = '경기도'
    elif splitaddr[0] == '강원도':
        splitaddr[0] = '강원특별자치도'
    elif splitaddr[0] == '서울':
        splitaddr[0] = '서울특별시'
    elif splitaddr[0] == '전북':
        splitaddr[0] = '전라북도'
    elif splitaddr[0] == '전남':
        splitaddr[0] = '전라남도'
    elif splitaddr[0] == '경북':
        splitaddr[0] = '경상북도'
    elif splitaddr[0] == '경남':
        splitaddr[0] = '경상남도'
    elif splitaddr[0] == '부산':
        splitaddr[0] = '부산광역시'
    elif splitaddr[0] == '대구':
        splitaddr[0] = '대구광역시'
    elif splitaddr[0] == '인천':
        splitaddr[0] = '인천광역시'
    elif splitaddr[0] == '광주':
        splitaddr[0] = '광주광역시'
    elif splitaddr[0] == '대전':
        splitaddr[0] = '대전광역시'
    elif splitaddr[0] == '울산':
        splitaddr[0] = '울산광역시'
    elif splitaddr[0] == '충북':
        splitaddr[0] = '충청북도'
    elif splitaddr[0] == '충남':
        splitaddr[0] = '충청남도'
    elif splitaddr[0] == '제주':
        splitaddr[0] = '제주특별자치도'
    if '창원시' in splitaddr[1]:
        splitaddr[1] = '창원시'
    elif '당진군' in splitaddr[1]:
        splitaddr[1] = '당진시'
    elif '청원군' in splitaddr[1]:
        splitaddr[1] = '청주시'
    kdaddr.append(' '.join(splitaddr))
print(kdaddr)

dfaddrkd = pd.DataFrame({'행정구역':kdaddr})
dfaddrkd = dfaddrkd['행정구역'].value_counts()

print(dfaddrsc)
print("-" * 50)
print(dfaddrkd)

filename4 = 'KndgtAddr.csv'
filename5 = 'SchlAddr.csv'
dfaddrkd.to_csv(filename4, encoding='utf-8')
dfaddrsc.to_csv(filename5, encoding='utf-8')