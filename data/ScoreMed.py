#!/usr/bin/env python

import pandas as pd


filename1 = 'HosAddr.csv'
filename2 = 'KorPop.csv'
hosaddr = pd.read_csv(filename1, encoding='utf-8')
korpop = pd.read_csv(filename2, encoding='utf-8')

print(hosaddr.head())
print(korpop.head())

# 인구 만명당 병원수

imsi = [0 for i in range (len(korpop))]
scoremed = pd.DataFrame({'행정구역':korpop['행정구역'], 'count':imsi})
# print(scoremed)

merged = pd.merge(scoremed, hosaddr[['행정구역', 'count']], on='행정구역', how='left')
merged = merged.drop('count_x', axis=1)
merged.rename(columns={'count_y':'count'}, inplace=True)
merged = merged.fillna(0)
merged = merged.astype({'count':'int'})

# 인구증감률이 양수라면 1.1을, 인구 증감률이 평균보다 낮으면 0.9의 weight를 줌
for i in range (len(korpop)):
    merged.loc[i, 'count'] /= korpop.loc[i, 'totpertt22']
    if korpop.loc[i, 'kidrate'] >= 0:
        merged.loc[i, 'count'] *= 1.1
    elif korpop.loc[i, 'kidrate'] < korpop['kidrate'].mean():
        merged.loc[i, 'count'] *= 0.9

merged = merged.sort_values(by='count', ascending=True, ignore_index=True)
print(merged)
score = 0
med = []
merged['is_same'] = (merged['count'] == merged['count'].shift(1))
merged['is_same'] = merged['is_same'].fillna(False)
for i in range (len(merged)):
    if merged.loc[i, 'count'] == 0:
        med.append(score)
    else:
        if merged.loc[i, 'is_same'] == False:
            score += 1
        med.append(score)
merged['score'] = med
merged['conscore'] = round(merged['score'] / 183 * 100, 2)

merged = merged.sort_values(by='행정구역', ascending=True, ignore_index=True)
scoremed = scoremed.sort_values(by='행정구역', ascending=True, ignore_index=True)

scoremed['count'] = merged['conscore']
scoremed.rename(columns={'count':'score'}, inplace=True)

print('-' * 50)
print(scoremed)

filename = 'ScoreMed.csv'
scoremed.to_csv(filename, encoding='utf-8', index=False)