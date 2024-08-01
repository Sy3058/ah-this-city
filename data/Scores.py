#!/usr/bin/env python

import pandas as pd

filename = 'KorPop.csv'
filename1 = 'ScoreMed.csv'
filename2 = 'ScoreEdu.csv'
filename3 = 'ScoreSaf.csv'
korpop = pd.read_csv(filename, encoding='utf-8')
scoremed = pd.read_csv(filename1, encoding='utf-8')
scoreedu = pd.read_csv(filename2, encoding='utf-8')
scoresaf = pd.read_csv(filename3, encoding='utf-8')

# print(scoremed)
# print(scoreedu)
# print(scoresaf)

scores = pd.DataFrame({'loc':korpop['행정구역'], 'med':scoremed['score'], 'edu':scoreedu['score'], 'saf':scoresaf['score']})

rank = [i+1 for i in range(len(scores))]
scores = scores.sort_values(by='med', ascending=False, ignore_index=True)
scores['medrank'] = rank
scores = scores.sort_values(by='edu', ascending=False, ignore_index=True)
scores['edurank'] = rank
scores = scores.sort_values(by='saf', ascending=False, ignore_index=True)
scores['safrank'] = rank

tot = scores['med'] + scores['edu'] + scores['saf']
scores['tot'] = tot

print(scores)

# filename = 'scores.csv'
# scores.to_csv(filename, encoding='utf-8', index =False)