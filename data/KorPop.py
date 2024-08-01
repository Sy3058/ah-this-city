#!/usr/bin/env python

import pandas as pd

filename1 = 'pop2122.csv'
filename2 = 'KorDiv.csv'
filename3 = 'PopDense.csv'

pop = pd.read_csv(filename1, encoding='utf-8')
kordiv = pd.read_csv(filename2, encoding='utf-8', dtype=object)
dense = pd.read_csv(filename3, encoding='utf-8')

korpop = pd.DataFrame(columns=pop.columns)

for idx, row in pop.iterrows():
    if row['행정구역'] in kordiv['행정구역'].values:
        korpop = pd.concat([korpop, row.to_frame().T], ignore_index=True)

korpop.drop('Unnamed: 0', axis=1, inplace=True) # 연령구간인구수와 0~9세 데이터가 동일하므로 지워줌

korpop['totpertt21'] = korpop['tot21']/10000 # 인구 만명당...
korpop['totpertt22'] = korpop['tot22']/10000
korpop['tidrate'] = (korpop['tot22'] - korpop['tot21'])/korpop['tot21'] # 총인구수 증감률
korpop['kidrate'] = (korpop['kid22'] - korpop['kid21'])/korpop['kid21'] # increase/decrease rate = after - before / before

increase = 0
for i in range (len(korpop)):
    if korpop.loc[i, 'kidrate'] >= korpop['kidrate'].mean():
        # print(korpop.iloc[i])
        increase += 1

# print(korpop['kidrate'].mean())
# -0.069
# print(korpop['tidrate'].mean())
# -0.007
korpop = korpop.sort_values(by='행정구역', ascending=True, ignore_index=True)

density = []
location = []
for i in range (len(dense)):
    for j in range (len(korpop)):
        if dense.loc[i, '행정구역별'] == korpop.loc[j, '행정구역']:
            location.append(korpop.loc[j,'행정구역'])
            density.append(dense.loc[i, '인구밀도'])
imsi = [0 for i in range (len(korpop))]
korpop['density'] = imsi
for i in range (len(korpop)):
    for j in range (len(location)):
        if location[j] == korpop.loc[i, '행정구역']:
            korpop.loc[i, 'density'] = density[j]
print(korpop)

filename = 'KorPop.csv'
korpop.to_csv(filename, encoding='utf-8', index =False)