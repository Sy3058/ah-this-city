#!/usr/bin/env python

import pandas as pd

filename = 'KorPop.csv'
filename1 = '2020TrafficAccident.csv'

korpop = pd.read_csv(filename, encoding='utf-8')
T22 = pd.read_csv(filename1, encoding='utf-8')

# print(korpop)
# print(T22)

addr = []
for i in range (len(T22)):
    splitaddr = [T22.loc[i,'시도'], T22.loc[i, '시군구']]
    if splitaddr[0] == '세종':
        splitaddr[0] = '세종특별자치시'
    if splitaddr[1] == '군위군':
        splitaddr[0] = '대구광역시'
    elif splitaddr[0] == '경기':
        splitaddr[0] = '경기도'
    elif '강원' in splitaddr[0]:
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
    if splitaddr[1] == '창원시(통합)':
        splitaddr[1] = '창원시'
    addr.append(' '.join(splitaddr))

T22['행정구역'] = addr
# print(T22)

T22 = T22.sort_values(by='행정구역', ascending=True, ignore_index=True)
korpop = korpop.sort_values(by='행정구역', ascending=True, ignore_index=True)


death = []
critical = []
location = []
for i in range (len(T22)):
    for j in range (len(korpop)):
        if korpop.loc[j, '행정구역'] == T22.loc[i, '행정구역']:
            location.append(T22.loc[i, '행정구역'])
            death.append(T22.loc[i, '사망자수'])
            critical.append(T22.loc[i, '중상자수'])

# filename = 'imsi.csv'
# T22.to_csv(filename, encoding='utf-8', index=False)
# filename1 = 'imsi2.csv'
# korpop.to_csv(filename1, encoding='utf-8', index=False)

imsi = pd.DataFrame({'행정구역':location, 'death':death, 'critical':critical})

imsi['harm'] = imsi['death'] + imsi['critical']
# print(imsi)

for i in range (len(imsi)):
    imsi.loc[i, 'harm'] /= korpop.loc[i, 'totpertt22']
    if korpop.loc[i, 'kidrate'] >= 0:
        imsi.loc[i, 'harm'] *= 1.1
    elif korpop.loc[i, 'kidrate'] < korpop['kidrate'].mean():
        imsi.loc[i, 'harm'] *= 0.9

imsi = imsi.sort_values(by='harm', ascending=True, ignore_index=True)
# print(imsi)

score = 0
saf = []
imsi['is_same'] = (imsi['harm'] == imsi['harm'].shift(1))
imsi['is_same'] = imsi['is_same'].fillna(False)
for i in range (len(imsi)):
    if imsi.loc[i, 'harm'] == 0:
        saf.append(score)
    else:
        if imsi.loc[i, 'is_same'] == False:
            score += 1
        saf.append(score)
imsi['score'] = saf
imsi['conscore'] = round(imsi['score'] / 198 * 100, 2)
print(imsi)

filename = 'Traffic.csv'
imsi.to_csv(filename, encoding='utf-8', index=False)