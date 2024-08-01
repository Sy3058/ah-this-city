#!/usr/bin/env python

import pandas as pd

filename = 'KorPop.csv'
filename1 = 'KndgtAddr.csv'
filename2 = 'SchlAddr.csv'
kdaddr = pd.read_csv(filename1, encoding='utf-8')
scaddr = pd.read_csv(filename2, encoding='utf-8')
korpop = pd.read_csv(filename, encoding='utf-8')

# print(kdaddr.head())
# print(scaddr.head())
# print(korpop.head())

imsi = [0 for i in range (len(korpop))]
scoreedu = pd.DataFrame({'행정구역':korpop['행정구역'], 'count':imsi})
# print(scoreedu)

kdaddr = kdaddr.sort_values(by='행정구역', ascending=True, ignore_index=True)
scaddr = scaddr.sort_values(by='행정구역', ascending=True, ignore_index=True)

scaddr['count'] = scaddr['count'] + kdaddr['count']

merged = pd.merge(scoreedu, scaddr[['행정구역', 'count']], on='행정구역', how='left')
merged = merged.drop('count_x', axis=1)
merged.rename(columns={'count_y':'count'}, inplace=True)
merged = merged.fillna(0)
merged = merged.astype({'count':'int'})
# print(merged)

# 인구증감률이 양수라면 1.1을, 인구 증감률이 평균보다 낮으면 0.9의 weight를 줌
for i in range (len(korpop)):
    # merged.loc[i, 'count'] /= korpop.loc[i, 'density']
    if korpop.loc[i, 'kidrate'] >= 0:
        # what a u doing?? where a u?? can u ask me?
        merged.loc[i, 'count'] *= 1.1
    elif korpop.loc[i, 'kidrate'] < korpop['kidrate'].mean():
        merged.loc[i, 'count'] *= 0.9

merged = merged.sort_values(by='count', ascending=True, ignore_index=True)
score = 0
edu = []
merged['is_same'] = (merged['count'] == merged['count'].shift(1))
merged['is_same'] = merged['is_same'].fillna(False)
for i in range (len(merged)):
    if merged.loc[i, 'count'] == 0:
        edu.append(score)
    else:
        if merged.loc[i, 'is_same'] == False:
            score += 1
        edu.append(score)
merged['score'] = edu
merged['conscore'] = round(merged['score'] / 198 * 100, 2)
print(merged)

merged = merged.sort_values(by='행정구역', ascending=True, ignore_index=True)
scoreedu = scoreedu.sort_values(by='행정구역', ascending=True, ignore_index=True)

scoreedu['count'] = merged['conscore']
scoreedu.rename(columns={'count':'score'}, inplace=True)

print('-' * 50)
print(scoreedu)

filename = 'ScoreEdu.csv'
scoreedu.to_csv(filename, encoding='utf-8', index=False)