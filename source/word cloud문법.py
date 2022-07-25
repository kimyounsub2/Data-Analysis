# word cloud(tag cloud)
# 문서에 언급된 단어들의 빈도수를 파악해서 빈도수가 높은 단어 (키워드)일 
# 수록 크게 빈도수가 낮은 단어일 수록 작게 표현하는 
# tag cloud에서는 tag가 키워드
read = 'C:/Users/A/Desktop/youn/python_day4/data/wctest.txt'
text=open(read,encoding='utf-8').read()
from wordcloud import WordCloud

# 텍스트인 경우
# stopwords = 불용어 리스트(빈도수 1)
wordcloud = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
                      background_color='white',
                      stopwords=['analysis','big']).generate(text)

#리스트인경우 문자열로 변환
text = ' '.join(['워드클라우드','워드클라우드','python','big'])

import matplotlib.pyplot as plt
plt.figure(figsize=(10,10)) # 이미지 사이즈
# wordcloud 이미지 출력
# 이미지의 경계선 계단현상을 보간(interpolation)해서 부드럽게 표현
plt.imshow(wordcloud, interpolation='lanczos')
plt.axis('off') # x, y축 숫자 제거

# 파일저장
plt.savefig('wordcloud.png')

wordcloud = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
                      background_color='white',
                      stopwords=['analysis','big'],
                      width=800, height=400).generate(text)

wordcloud.to_file('C:/Users/A/Desktop/youn/python_day4/wordcloud2.png')
# (단어:빈도수) 사전
wordcloud.process_text(text)

#%% Counter 기반 (단어:빈도수) 사전 생성해서 word cloud
read = 'C:/Users/A/Desktop/youn/python_day4/data/news.txt'

f = open(read,'r',encoding='utf-8')
corpus = f.readlines()
f.close()

corpus_morph=[]
for doc in corpus:
    lst=doc.split()    
    #글자수(음절)가 3이상이면 포함
    nou=[n for n in lst if len(n) >=3] #n이 분할된(split) 단어
    corpus_morph.append(nou)

corpus_morph
'''
[['현충원', '방명록'], ['서울시', '대한민국', '당선자', '코로나', '서울시']]
'''

# 문자열
# Counter('abcdeabcdabc') : 문자마다 개수 집계

from collections import Counter
# 단일리스트
# Counter('abcdeabcdabc') : 단어요소마다 개수 집계
counter = Counter(['현충원','방명록'])

# 다중리스트
# 단어들을 가지는 다중리스트를 Counter에 입력
# 단어 : 빈도수의 사전을 가지는 Counter

counter = Counter()
for m in corpus_morph:
    counter.update(m) # 카운터에 추가
    
# elements() : 단어들
# sorted() : 정렬 
print(sorted(counter.elements()))

# {단어:빈도수} 사전
# 생성함수로 generate_from_frequencies() 사용
# stopwords 미반영, 사전에 방명록 항목제거
tf = dict(counter.most_common(3))
# del tf('방명록')
tf.pop('방명록')
wordcloud = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
                      background_color='white',
                      stopwords=['방명록']).generate_from_frequencies(tf)

plt.figure(figsize=(15,15)) # 이미지 사이즈
# wordcloud 이미지 출력
# 이미지의 경계선 계단현상을 보긴(interpolation)해서 부드럽게 표현
plt.imshow(wordcloud, interpolation='lanczos')
plt.axis('off')

#%% DataFrame word cloud
# generate_from_frequencies(사전)
# DataFrame -> 사전
import pandas as pd
df = pd.DataFrame({'keyword':['서울시','현충원','방명록'],
                   'count':[2,1,1]})

df = df.drop(2)
    
    
# 결과 이상
# 예를 들어 벨류값['서울시','현충원','방명록'] 도 사전구조로 변환
# tf = df.to_dict()
# 단어사전 {'서울시':2, '현충원':1, '방명록':1}을 추출
tf = df.set_index('keyword').to_dict()['count']
wordcloud = WordCloud(font_path='c:/windows/fonts/malgun.ttf',
                      background_color='white'
                      ).generate_from_frequencies(tf)

#%% Folium
# 위치정보를 시각화하고 
# 지리정보데이터(GIS)를 처리하는데 유용한 라이브러리 패키지
# GIS 위치 좌표
# 위도(latitude)'와 '경도(longitude)


import folium

#맵을 생성하면서 서울특별시청의 값을 중심값으로 하여 지도를 생성한다
map_osm = folium.Map(location=[37.566345, 126.977893],
                     zoom_start=14)
map_osm.save('map.html')

# 마커,popup(클릭), tootip(호버) 표시
map_osm = folium.Map(location=[37.566345, 126.977893],
                     zoom_start=14)
folium.Marker(location=[37.566345,126.977893],
              popup='서울특별시청',
              tooltip ='서울시청').add_to(map_osm)
map_osm.save('C:/Users/A/Desktop/youn/python_day4/map.html')

#%%
# 마커 아이콘 변경
icon = folium.Icon(color='red',icon='home')

# 마커,popup(클릭), tootip(호버) 표시
# CircleMarker 원반경(100), popup(클릭),tooltip(호버) 표시
folium.Marker(location=[37.566345,126.977893],
              popup='서울특별시청',
              tooltip ='서울시청',
              icon=icon).add_to(map_osm)
folium.CircleMarker(location=[37.566345,126.977893],
                    popup='서울시청부근',
                    tooltip='서울시청부근',
                    radius=100,
                    color='red',
                    fill_color='green').add_to(map_osm)
map_osm.save('C:/Users/A/Desktop/youn/python_day4/map2.html')

#%% 덕수궁 위처정보를 CricleMarker 시각화 하기
map_osm = folium.Map(location=[37.566202, 126.978181],
                     zoom_start=14)

folium.Marker(location=[37.566202,126.978181],
              popup='서울특별시 중구 세종대로',
              tooltip ='덕수궁',
              icon=icon).add_to(map_osm)

folium.CircleMarker(location=[37.566202,126.978181],
                    popup='서울특별시 중구 세종대로',
                    tooltip='덕수궁',
                    radius=100,
                    color='red',
                    fill_color='green').add_to(map_osm)
map_osm.save('C:/Users/A/Desktop/youn/python_day4/map3.html')

#%% 다중위치,마커
import folium
import numpy as np

lats= [37.493922,37.505675,37.471711]
longs= [127.061026,127.047883,127.899220]
#기준좌표는 위치의 평균
map_osm = folium.Map(location=[np.mean(lats),np.mean(longs)],
           zoom_start=9)

for loc in range(3):
    # 각 위치 loc에 대한 마커 생성 map에 추가
    folium.Marker(location=[lats[loc], longs[loc]],
                  popup='popup',tooltip='tooltip').add_to(map_osm)


map_osm.save('C:/Users/A/Desktop/youn/python_day4/map4.html')

#%% 다중위치(파일), 마커
import pandas as pd
read = 'C:/Users/A/Desktop/youn/python_day4/data/latslongs.csv'
df = pd.read_csv(read)

map_osm = folium.Map(location=[df['latitude'].mean(),
                               df['longitude'].mean()],
           zoom_start=9)

for loc in range(3):
    # 각 위치 loc에 대한 마커 생성 map에 추가
    folium.Marker(location=[df['latitude'][loc], df['longitude'][loc]],
                  popup='popup',tooltip='tooltip').add_to(map_osm)
    
location = list(zip(df['latitude'],df['longitude']))

for loc in range(3):
    # 각 위치 loc에 대한 마커 생성 map에 추가
    folium.Marker(location=location[loc],
                  popup='popup',tooltip='tooltip').add_to(map_osm)

map_osm.save('C:/Users/A/Desktop/youn/python_day4/map6.html')

#%% 다중마커의 MarkerCluster 처리

read = 'C:/Users/A/Desktop/youn/python_day4/data/공공자전거 대여소 정보_201905.xlsx'
bike=pd.read_excel(read)
bike.info()

#1. folium Map 생성 위도,경도 평균
bmap = folium.Map(location=[bike['위도'].mean(), bike['경도'].mean()],
                    zoom_start=11)


#2. 마커들을 마커배열안에 넣는 과정
#marker_cluster 변수는 마커들의 배열 생성하고 
#folium Map에 추가된  MarkerCluster의 Map
from folium.plugins import MarkerCluster
marker_cluster = MarkerCluster().add_to(bmap)

#3. 마커를 생성하고 marker_cluster에 추가
#모든 거치대수를 문자형으로 변환 
#popup 인자에 +로 문자열 연결
#bike['거치대수']가 정수이므로 + 결합을 위해서 문자열로 변환
#'거치대수 :' + 5 #오류
# '거치대수 :' + str(5) # 해결
bike['거치대수']=[str(value) for value in bike['거치대수']]

#반복문으로 데이터를 기반으로 마커를 생성
#마커를 marker_cluster에 추가
for n in bike.index:  
        folium.Marker(location=[bike['위도'][n], bike['경도'][n]],
                      popup='거치대수 :' + bike['거치대수'][n],
                     tooltip=bike['대여소명'][n]).add_to(marker_cluster)
         
bmap.save('C:/Users/A/Desktop/youn/python_day4/mapClusterMarker.html')

#%% 
# 행정구역이 MultiPolygon 형식으로 입력되어 있는 JSON 데이터를 불러들여 지도에 표시
# geoJSON 형식은 지도상의 경계 영역 등을 표시하기에 효율적 

# JSON 형식 행정구역(서울구들) 데이터

import json
map_osm = folium.Map(location=[37.566345, 126.977893])
read = 'C:/Users/A/Desktop/youn/python_day4/data/geo.json'
file = open(read, 'r', encoding='utf-8').read()

jsonData = json.loads(file)
#name은 대략 주자
folium.GeoJson(jsonData, name='jsondata').add_to(map_osm)

map_osm.save('C:/Users/A/Desktop/youn/python_day4/mapjson.html')
