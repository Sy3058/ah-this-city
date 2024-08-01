#!/usr/bin/env python

import pandas as pd

filename1 = 'kor_div_code.csv'
filename2 = 'kor_div_code2022.csv'
div23 = pd.read_csv(filename1, encoding='utf-8', dtype=object)
div22 = pd.read_csv(filename2, encoding='utf-8', dtype=object)

print(div23.info())
div23 = div23[['시도코드', '시도명칭', '시군구코드', '시군구명칭']]
# div22 = div22[['시도코드', '시도명칭', '시군구코드', '시군구명칭']]

# print(div23.head())
# print('-' * 50)
# print(div22.head())
# print('-' * 50)

div23 = div23.drop_duplicates(['시군구명칭'], keep='first', ignore_index = True)
# div22 = div22.drop_duplicates(['시군구명칭'], keep='first', ignore_index = True)

code = []

for i in range (len(div23)):
    code.append(div23.loc[i, '시도코드'] + div23.loc[i, '시군구코드'])

# print(code)

kordiv = pd.DataFrame({'주소코드':code, '시도명칭':div23['시도명칭'], '시군구명칭':div23['시군구명칭']})
print(kordiv)

kordiv[['시군구명칭', 'nothing']] = kordiv['시군구명칭'].str.split(' ', n=1, expand=True)
kordiv = kordiv.drop_duplicates(['시군구명칭'], keep='first', ignore_index = True)
kordiv = kordiv.drop('nothing', axis=1)
for i in range (len(kordiv)):
    if kordiv.loc[i, '주소코드'][-1] != '0':
        kordiv.loc[i, '주소코드'] = kordiv.loc[i, '주소코드'][:4] + '0'

kordiv['행정구역'] = kordiv.apply(lambda row: ' '.join([row['시도명칭'], row['시군구명칭']]), axis=1)

filename = 'KorDiv.csv'
kordiv.to_csv(filename, encoding='utf-8')


# 군위군이 2022년에는 경북이었는데 23년에는 대구로 편입됨
# 모든 시군구는 2023년 기준으로 보겠음!!