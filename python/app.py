from fastapi import FastAPI, Query
from bson.objectid import ObjectId
from pymongo import mongo_client
from starlette.responses import Response, FileResponse
import pydantic
from pydantic import BaseModel
from typing import List
from database import db_conn
import os.path
import requests, json
import pandas as pd
import matplotlib.pyplot as plt

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str
plt.rcParams['font.family'] = 'NanumBarunGothic'

app = FastAPI()

db = db_conn()
session = db.sessionmaker()

BASE_DIR = os.path.dirname(os.path.dirname(os.path.relpath("./")))
secret_file = os.path.join(BASE_DIR, '../secret.json')
IMAGE_DIR = os.path.join(BASE_DIR, 'imagefolder')
os.makedirs(IMAGE_DIR, exist_ok=True)

with open(secret_file) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    try:
        return secrets[setting]
    except KeyError:
        errorMsg = "Set the {} environment variable.".format(setting)
        return errorMsg

def get_addr(sampleaddr):
    addr = []
    for i in range (len(sampleaddr)):
        splitaddr = sampleaddr[i].split()[:2]
        if splitaddr[0] == '세종특별자치시':
            splitaddr[1] = '세종시'
        elif splitaddr[0] == '경기':
            splitaddr[0] = '경기도'
        elif splitaddr[0] == '강원도':
            splitaddr[0] = '강원특별자치도'
        elif splitaddr[0] == '서울':
            splitaddr[0] = '서울특별시'
        elif splitaddr[0] == '전북':
            splitaddr[0] = '전라북도'
        elif splitaddr[0] == '전북특별자치도':
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
        elif splitaddr[1] == '군위군':
            splitaddr[0] = '대구광역시'
        addr.append(' '.join(splitaddr))
    return addr

def get_score(addr):
    korpop = pd.DataFrame(popcol.find({}, {"_id":0}))
    dfaddr = pd.DataFrame({'행정구역': addr})
    dfaddr = dfaddr['행정구역'].value_counts().reset_index()
    dfaddr.columns = ['행정구역', 'count']

    imsi = [0 for i in range (len(korpop))]
    scoreenv = pd.DataFrame({'행정구역':korpop['행정구역'], 'count':imsi})

    merged = pd.merge(scoreenv, dfaddr[['행정구역', 'count']], on='행정구역', how='left')
    merged = merged.drop('count_x', axis=1)
    merged.rename(columns={'count_y':'count'}, inplace=True)
    merged = merged.fillna(0)
    merged = merged.astype({'count':'int'})

    for i in range (len(korpop)):
        if korpop.loc[i, 'kidrate'] >= 0:
            merged.loc[i, 'count'] *= 1.1
        elif korpop.loc[i, 'kidrate'] < korpop['kidrate'].mean():
            merged.loc[i, 'count'] *= 0.9

    merged = merged.sort_values(by='count', ascending=True, ignore_index=True)
    score = 0
    env = []
    merged['is_same'] = (merged['count'] == merged['count'].shift(1))
    merged['is_same'] = merged['is_same'].fillna(False)
    for i in range (len(merged)):
        if merged.loc[i, 'count'] == 0:
            env.append(score)
        else:
            if merged.loc[i, 'is_same'] == False:
                score += 1
            env.append(score)
    merged['score'] = env
    merged = merged.sort_values(by='행정구역', ascending=True, ignore_index=True)
    scoreenv = scoreenv.sort_values(by='행정구역', ascending=True, ignore_index=True)
    merged['conscore'] = round(merged['score'] / max(merged['score']) * 100, 2)

    scoreenv['count'] = merged['conscore']
    scoreenv.rename(columns={'count':'score'}, inplace=True)
    
    return scoreenv

mycolors=['#1D6165', '#389576', '#85C670', '#a5d6a7']

def make_graph(data, category):
    locations = [item['loc'] for item in data]
    edu_scores = [item['edu'] for item in data]
    env_scores = [item['env'] for item in data]
    med_scores = [item['med'] for item in data]
    saf_scores = [item['saf'] for item in data]
    tot_scores = [item['tot'] for item in data]

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.15
    index = range(len(locations))

    ax.bar(index, edu_scores, bar_width, label='교육', color=mycolors[0])
    ax.bar([i + bar_width for i in index], saf_scores, bar_width, label='안전', color=mycolors[1])
    ax.bar([i + 2 * bar_width for i in index], med_scores, bar_width, label='의료', color=mycolors[2])
    ax.bar([i + 3 * bar_width for i in index], env_scores, bar_width, label='환경', color=mycolors[3])

    ax.set_xlabel('Top3 지역')
    ax.set_xticks([i + 1.5 * bar_width for i in index])
    ax.set_xticklabels(locations, rotation=45, ha='right')
    ax.legend()

    # 그래프 이미지 저장
    image_path = os.path.join(IMAGE_DIR, f'{category}_graph.png')
    plt.savefig(image_path, dpi=400, bbox_inches='tight')

    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    return image_bytes

def make_graph_tot(data, category):
    locations = [item['loc'] for item in data]
    edu_scores = [item['edu'] for item in data]
    env_scores = [item['env'] for item in data]
    med_scores = [item['med'] for item in data]
    saf_scores = [item['saf'] for item in data]
    tot_scores = [item['tot'] for item in data]

    # 그래프 생성
    fig, ax = plt.subplots(figsize=(12, 6))
    bar_width = 0.6
    index = range(len(locations))

    bottom = [0] * len(locations)
    ax.barh(index, edu_scores, bar_width, label='교육', left=bottom, color=mycolors[0])
    bottom = [bottom[i] + edu_scores[i] for i in range(len(locations))]
    ax.barh(index, saf_scores, bar_width, label='안전', left=bottom, color=mycolors[1])
    bottom = [bottom[i] + saf_scores[i] for i in range(len(locations))]
    ax.barh(index, med_scores, bar_width, label='의료', left=bottom, color=mycolors[2])
    bottom = [bottom[i] + med_scores[i] for i in range(len(locations))]
    ax.barh(index, env_scores, bar_width, label='환경', left=bottom, color=mycolors[3])

    ax.set_xlabel('종합 점수')
    ax.set_yticks(index)
    ax.set_yticklabels(locations)
    ax.legend()

    # 그래프 이미지 저장
    image_path = os.path.join(IMAGE_DIR, f'{category}_graph.png')
    plt.savefig(image_path, dpi=400, bbox_inches='tight')

    with open(image_path, 'rb') as f:
        image_bytes = f.read()
    
    return image_bytes

opt = {1: "edu", 2: "saf", 3: "med", 4: "env"}

class SearchOption(BaseModel):
    addr: str
    option: List[int]

HOSTNAME = get_secret("Local_Mongo_Hostname")
USERNAME = get_secret("Local_Mongo_Username")
PASSWORD = get_secret("Local_Mongo_Password")

client = mongo_client.MongoClient(f'mongodb://{USERNAME}:{PASSWORD}@{HOSTNAME}')
print('Connected to Mongodb...')

mydb = client['project']
mycol = mydb['scores']
newcol = mydb['totalscores']
popcol = mydb['korpop']

@app.get('/')
async def healthcheck():
    return "OK"

# api에서 값을 가져와 env에 점수 저장
@app.get('/getapidata')
async def getAPIData():
    all_items = []

    serviceKey = get_secret("data_apiKey")
    page = 1
    recordcount = 1000
    placecd = "A003"

    url = f"https://apis.data.go.kr/1741000/pfc2/pfc/getPfctInfo2?serviceKey={serviceKey}&pageIndex={page}&recordCountPerPage={recordcount}&instlPlaceCd={placecd}"
    response = requests.get(url)
    contents = response.text
    apidict = json.loads(contents)
    total_pages = apidict['response']['body']['totalPageCnt']

    while page <= total_pages:
        # OpenAPI 엔드포인트 URL
        url = f"https://apis.data.go.kr/1741000/pfc2/pfc/getPfctInfo2?serviceKey={serviceKey}&pageIndex={page}&recordCountPerPage={recordcount}&instlPlaceCd={placecd}"
        
        response = requests.get(url)
        contents = response.text
        apidict = json.loads(contents)
        
        # 현재 페이지의 items 추출
        items = apidict['response']['body']['items']
        all_items.extend(items)
        
        page += 1
    
    envaddr = []
    for i in range (len(all_items)):
        envaddr.append(all_items[i]['rgnCdNm'])
    
    envaddr = get_addr(envaddr)
    dfenvaddr = get_score(envaddr)

    data = mycol.find({}, {"_id":0})
    i = 0
    for doc in data:
        env = dfenvaddr.loc[i, 'score']
        i += 1
        doc["env"] = env

        newcol.update_one(
            {'loc': doc['loc']},
            {'$set': doc},
            upsert=True
        )
    
    result = list(newcol.find({}, {"_id": 0}))

    return result

# total 값 구하기
@app.get('/gettotal')
async def getTotal():
    data = newcol.find({}, {"_id": 0})
    # newcol에 기존 데이터 저장하고 tot 필드 추가
    for doc in data:
        tot = (doc["med"] + doc["edu"] + doc["saf"] + doc["env"])
        doc["tot"] = round(tot,2)
        newcol.update_one(
            {'loc': doc['loc']},
            {'$set': doc},
            upsert=True
        )

    # newcol에서 모든 데이터 가져오기
    result = list(newcol.find({}, {"_id": 0}))

    return result

@app.get('/select')
async def Select():
    data = list(newcol.find({}, {"_id":0}))
    return data

# 종합 top10
@app.get('/select/top10')
async def SelectTop10():
    data = list(newcol.find({}, {"_id":0}).sort('tot', -1).limit(10))
    
    return data

# 종합 top10 graph 저장 및 반환
@app.get('/select/top10/graph')
async def SelectTop10Graph():
    data = list(newcol.find({}, {"_id": 0}).sort('tot', -1).limit(10))
    
    data = sorted(data, key=lambda x: x['tot'])
    top_graph = make_graph_tot(data, "top10")

    # 이미지 바이트 스트림 반환
    return Response(content=top_graph, media_type='image/png')

# 지수별 top3
@app.get('/select/categorytop3')
async def SelectCategoryTop3():
    med_data = list(newcol.find({}, {"_id":0}).sort('med', -1).limit(3))
    env_data = list(newcol.find({}, {"_id":0}).sort('env', -1).limit(3))
    edu_data = list(newcol.find({}, {"_id":0}).sort('edu', -1).limit(3))
    saf_data = list(newcol.find({}, {"_id":0}).sort('saf', -1).limit(3))

    return med_data, env_data, edu_data, saf_data

# 지수별 top3 graph 저장
@app.get('/select/categorytop3/graphs')
async def SelectCategoryTop3Graphs():
    med_data = list(newcol.find({}, {"_id":0}).sort('med', -1).limit(3))
    env_data = list(newcol.find({}, {"_id":0}).sort('env', -1).limit(3))
    edu_data = list(newcol.find({}, {"_id":0}).sort('edu', -1).limit(3))
    saf_data = list(newcol.find({}, {"_id":0}).sort('saf', -1).limit(3))
    
    med_image = make_graph(med_data, "med")
    env_image = make_graph(env_data, "env")
    edu_image = make_graph(edu_data, "edu")
    saf_image = make_graph(saf_data, "saf")

    return "OK"

# 지수별 top3 graph 불러오기
@app.get('/select/categorytop3/graphs/{category}')
async def SelectCategoryTop3GraphsEach(category: str):
    # graphs에서 return해주는 med_image ~~ 를 받아오면 Response(content=f'{category}_graph.png, media_type='image/png')로 불러올수잇는듯..?
    image_path = os.path.join(IMAGE_DIR, f'{category}_graph.png')
    if os.path.exists(image_path):
        return FileResponse(image_path)
    else:
        return {'error': '해당하는 파일이 없습니다.'}

# 검색하기
@app.get('/search')
async def Search(addr: str=None, options: List[int] = Query(None)):
    data = list(newcol.find({}, {"_id": 0}))
    # addr = search_option.addr
    # options = search_option.option
    df = pd.DataFrame(data)
    df = df.round(2)
    if addr=="전체":
        filtered_data = [d for d in data]
    else:
        filtered_data = [d for d in data if d["loc"].split()[0] == addr]

    results = []
    for doc in filtered_data:
        if options:
            opttot = sum(doc[opt[i]] for i in options)
        else:
            opttot = doc['tot']
        results.append({"loc": doc["loc"], "opttot": opttot})
    if len(results) >= 10:
        sorted_results = sorted(results, key=lambda x: x["opttot"], reverse=True)
    else:
        sorted_results = sorted(results, key=lambda x: x["opttot"], reverse=True)

    dfsr = pd.DataFrame(sorted_results)
    
    merged = pd.merge(df, dfsr)
    merged = merged.sort_values(by = 'opttot', ascending=False, ignore_index=True)
    result = merged.to_dict(orient='index')

    return result