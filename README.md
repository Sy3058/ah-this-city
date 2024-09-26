# 👨‍👩‍👧‍👦아이 키우기 좋은 동네? "아!이 동네" 서비스

![Main Page](https://github.com/user-attachments/assets/52f2877d-350d-4622-ad87-ae135d575dd4)

## 📌목차

1. [프로젝트 소개](#project)
2. [개발 일정](#period)
3. [개발 환경](#environment)
4. [프로젝트 구조](#structure)
5. [페이지별 기능](#function)
6. [프로젝트 후기](#review)

<br>

## <span id="project">1. 프로젝트 소개</span>

- 지역별 교육, 안전, 의료, 환경 점수를 매겨 **종합 점수** 산출
- 요인 별로 **점수가 높은 순위** 확인 가능

<br>

## <span id="period">2. 개발 일정</span>

- 전체 개발 기간: 2024-04-15 ~ 2024-05-02

<br>

## <span id="environment">3. 개발 환경</span>

- Front: HTML, css, JavaScript
- Back: Node.js, FastAPI
- db: MongoDB
- 데이터 수집 및 정리: Python, 공공데이터포 OPEN API
- 디자인: Figma

<br>

## <span id="structure">4. 프로젝트 구조</span>

```
├── README.md
├── data/
├── node/
│   ├── public/
│   │   ├── category.html
│   │   ├── index.html
│   │   ├── logo.png
│   │   ├── search.html
│   │   ├── search-box.png
│   │   ├── styles.css
│   │   └── top10.html
│   ├── routes/
│   │   └── main.js
│   ├── app.js
│   └── package.json
└── python/
    ├── imagefolder/
    │
    ├── app.py
    ├── database.py
    ├── Makefile
    └── models.py
```

<br>

## <span id="function">5. 페이지별 기능</span>

### [메인 페이지]
![Team3_화면설계서_페이지_1](https://github.com/user-attachments/assets/90a6db2d-462f-476f-8e02-1aae190e14c2)

### [메인 페이지 - search]
![Team3_화면설계서_페이지_2](https://github.com/user-attachments/assets/c2a6ca30-8718-4851-b6b7-6a902cd04bec)

### [종합 순위 보기]
![Team3_화면설계서_페이지_3](https://github.com/user-attachments/assets/d74dacc5-a1e9-4040-8ea6-73a52be46d64)

### [지수별 순위 보기]
![Team3_화면설계서_페이지_4](https://github.com/user-attachments/assets/098c9262-1d88-45e1-acd6-b4e8eba5cbaf)

<br>

## <span id="review">6. 프로젝트 후기</span>

Back과 Front를 모두 구현해본 것이 처음이라 걱정이 많았는데 다행히 주어진 기한 내에 프로젝트를 끝낼 수 있었습니다. 주어진 데이터가 부족해 완벽히 원하던 결과를 얻었다고 할 순 없었지만 나름대로 인구수나 지역에 따른 편차를 해결해보고자 노력해보았습니다. 처음에 데이터 분석에 지나치게 오랜 시간을 써서 홈페이지 구현에는 별로 시간을 할애하지 못했던 것이 아쉽습니다. 또 아직 깃을 사용하는 것이 익숙하지 않아 모든 코딩이 끝난 후 백업 용도로만 쓰게 되었다는 것이 아쉽습니다. 코딩했던 기록을 남겼다면 추후 보완할 점을 확인하기 더 좋았을 것 같습니다. 부족한 것도 많지만 처음으로 온전히 끝마친 프로젝트였습니다. 이 프로젝트를 발판 삼아 더 많은 프로젝트를 진행해보고 싶습니다.
