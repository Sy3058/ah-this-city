#!/usr/bin/env python

import pandas as pd

filename1 = 'Population.csv'
filename2 = 'KorDiv.csv'

pop = pd.read_csv(filename1, encoding='utf-8')
kordiv = pd.read_csv(filename2, encoding='utf-8', dtype=object)

pop.drop('2020년_계_연령구간인구수', axis=1, inplace=True) # 연령구간인구수와 0~9세 데이터가 동일하므로 지워줌
pop.drop('2021년_계_연령구간인구수', axis=1, inplace=True)
pop.drop('2022년_계_연령구간인구수', axis=1, inplace=True)
pop.drop('2020년_계_총인구수', axis=1, inplace=True)
pop.drop('2020년_계_0~9세',axis=1,inplace=True)

pop[['nothing', 'citynumber']] = pop['행정구역'].str.split('(', n=1, expand=True)
pop.drop('nothing', axis=1, inplace=True)

for i in range (len(pop)):
    pop.loc[i, '행정구역'] = pop.loc[i, '행정구역'][:-13]
    pop.loc[i, 'citynumber'] = pop.loc[i, 'citynumber'].rstrip(')')
    if '00000000' in pop.loc[i, 'citynumber']:
        pop.drop(i, inplace=True)
    elif '000000' not in pop.loc[i, 'citynumber']:
        pop.drop(i, inplace=True)
    elif '세종' in pop.loc[i, '행정구역']:
        pop.loc[i, '행정구역'] = '세종특별자치시 세종시'
    elif '군위' in pop.loc[i, '행정구역']:
        pop.loc[i, '행정구역'] = '대구광역시 군위군'
pop = pop.reset_index(drop=True)

pop[['sido', 'gugun']] = pop['행정구역'].str.split(' ', n=1, expand=True)
for i in range (len(pop)):
    if pop.loc[i,'sido'] == '강원도':
        pop.loc[i,'sido'] = '강원특별자치도'
pop['행정구역'] = pop.apply(lambda row: ' '.join([row['sido'], row['gugun']]), axis=1)
pop.drop('sido', axis=1, inplace=True)
pop.drop('gugun', axis=1, inplace=True)
pop.drop('citynumber', axis=1, inplace=True)

# 2020년_계_총인구수,2020년_계_0~9세,2021년_계_총인구수,2021년_계_0~9세,2022년_계_총인구수,2022년_계_0~9세
for i in range (len(pop)):
    pop.loc[i, '2021년_계_총인구수'] = pop.loc[i, '2021년_계_총인구수'].replace(',','')
    pop.loc[i, '2021년_계_0~9세'] = pop.loc[i, '2021년_계_0~9세'].replace(',', '')
    pop.loc[i, '2022년_계_총인구수'] = pop.loc[i, '2022년_계_총인구수'].replace(',', '')
    pop.loc[i, '2022년_계_0~9세'] = pop.loc[i, '2022년_계_0~9세'].replace(',', '')
pop = pop.astype({'2021년_계_총인구수':'int32','2021년_계_0~9세':'int32','2022년_계_총인구수':'int32','2022년_계_0~9세':'int32'})
pop = pop.rename(columns={'2021년_계_총인구수':'tot21', '2021년_계_0~9세':'kid21', '2022년_계_총인구수':'tot22','2022년_계_0~9세':'kid22'})
print(pop.info())

filename = 'pop2122.csv'
pop.to_csv(filename, encoding='utf-8')