#!/usr/bin/env python

import pandas as pd

filename = 'KorPop.csv'
filename1 = 'Traffic.csv'
filename2 = 'KoreaSecurityIndex.csv'

korpop = pd.read_csv(filename, encoding='utf-8')
traf = pd.read_csv(filename1, encoding='utf-8')
ksi = pd.read_csv(filename2, encoding='utf-8', index_col=0)

# print(traf)
# print(ksi)

imsi = [0 for i in range (len(korpop))]
scoreksi = pd.DataFrame({'행정구역':korpop['행정구역'], 'score':imsi})

addr = []
for i in range (len(ksi)):
    ksi.loc[i,'점수'] = ksi.loc[i,'점수'].replace('점','')
    splitaddr = [ksi.loc[i, '시도'], ksi.loc[i, '군구']]
    if splitaddr[0] == '강원도':
        splitaddr[0] = '강원특별자치도'
    addr.append(' '.join(splitaddr))

ksi['행정구역'] = addr
ksi = ksi.astype({'점수':'float'})

ksi = ksi.sort_values(by='점수', ascending=True, ignore_index=True)
for i in range (len(scoreksi)):
    for j in range (len(ksi)):
        if scoreksi.loc[i, '행정구역'] == ksi.loc[j, '행정구역']:
            scoreksi.loc[i, 'score'] = ksi.loc[j, '점수']

scoreksi = scoreksi.sort_values(by='score', ascending=True, ignore_index=True)

score = 0
saf = []
scoreksi['is_same'] = (scoreksi['score'] == scoreksi['score'].shift(1))
scoreksi['is_same'] = scoreksi['is_same'].fillna(False)
for i in range (len(scoreksi)):
    if scoreksi.loc[i, 'score'] == 0:
        saf.append(score)
    else:
        if scoreksi.loc[i, 'is_same'] == False:
            score += 1
        saf.append(score)

scoreksi['calscore'] = saf
scoreksi['conscore'] = round(scoreksi['calscore'] / 139 * 100, 2)
scoreksi = scoreksi.sort_values(by='행정구역', ascending=True, ignore_index=True)
traf = traf.sort_values(by='행정구역', ascending=True, ignore_index=True)

scoresaf = pd.DataFrame({'행정구역':korpop['행정구역'], 'score':traf['conscore']})
scoresaf['score'] += scoreksi['conscore']
scoresaf['score'] = round(scoresaf['score']/2, 2)

print(korpop)
# print(scoresaf)

filename = 'ScoreSaf.csv'
scoresaf.to_csv(filename, encoding='utf-8', index=False)