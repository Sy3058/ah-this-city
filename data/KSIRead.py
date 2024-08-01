#!/usr/bin/env python

import pandas as pd
from pandas import DataFrame

filename = 'KoreaSecurityIndex.csv'

myframe = pd.read_csv(filename, encoding='utf-8',index_col=0)
print('head() 메서드 결과')
print(myframe.head())
print('-' * 50)

score = []
for i in range (len(myframe)):
    score.append(int(myframe['순위'][i].rstrip('위')))

myframe['순위'] = score
myframe = myframe.sort_values(by='순위')
myframe = myframe.reset_index(drop=True)
print(myframe)

# # 검색하고 싶은 시군구 검색
# keyword = input("검색하고 싶은 시군구를 입력하세요(ex. 용인) : ").strip()
# for i in range (len(myframe)):
#     if keyword in myframe['군구'][i]:
#         print(myframe.loc[i])

print(len(myframe['점수']))