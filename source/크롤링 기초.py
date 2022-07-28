'''
미국 USD 환률 스크래핑(scraping)
naver 금융 -> 시장지표 
https://finance.naver.com/marketindex/
'''
url='https://finance.naver.com/marketindex/'
css_sel = '#exchangeList > li.on > a.head.usd > div > span.value'
#웹 크롤링
import requests, bs4
resp = requests.get(url)
resp.encoding 
html = resp.text
print(html)

#웹 스크래핑
#BeautifulSoup 파서 생성
bs = bs4.BeautifulSoup(html, 'html.parser')
#분리 요소들중 원하는 요소들 선택 추출
#tags = bs.select(css_sel)
#분리 요소들중 원하는 요소 선택 추출
tag = bs.select_one(css_sel)

#요소의 텍스트 추출
print('usd환률 = ',tag.text)
print('usd환률 = ',tag.getText())

#%% 웹 크롤링과 스크래핑

# HTTP 요청 모듈
import requests
# 크롤링을 할때 요청에서 requests를 사용

# get 요청
resp = requests.get('http://finance.naver.com')
# 응답상태 코드
resp.status_code # 200

# 응답을 문자열로 리턴
resp.text

# 한글 인코딩
resp.encoding

#%%
# post 요청(실제 get 요청)
# get params = 파라미터 사전
resp = requests.get('https://search.naver.com/search.naver',
                    params={'query':'corona'})

# post 오류
resp = requests.post('https://search.naver.com/search.naver',
                    data={'query':'corona'})

import json
# dic : 파이썬 딕셔너리 객체
dic = {'id':1, 'name':'kim','age':10}
resp = requests.post('http://httpbin.org/post',
                     data = json.dumps(dic))
resp.text
# 일반적으로
# json.dumps() : 딕셔너리의 구조를 유지하면서 문자열로 바꿔서 전달해야 한다.

#%% urllib.request(urllib는 파이썬 내장 모듈)
import urllib.request as req
resp = req.urlopen('https://www.naver.com/')
resp.status # 200

# 바이트 배열을 리턴
# resp.read() # 한글이 인코딩(예를 들면 xb3\xa0\xea\xb0), 바이트
# 바이트 배열을 문자열로 디코딩
resp.read().decode()

resp = req.urlopen('https://finace.naver.com/')
resp.status

resp.getheader('content-type')

#%% BeautifulSoup 1
import bs4

s = 'f_lst > ul > li:nth-child(2)'
s2 = 'f_list > ul > li:nth-child(2) > span'

# nth-of-type NotImlementedError
# :nth-child(2)를 제거

s2 = '#f_lst > ul > li > span'

html = open('test.html', encoding='utf-8')
# lxml, html.parser
soup = bs.BeautifulSoup(html,'html.parser')
# find(태그)
# 단일 요소 찾기
soup.find('h1') # 요소 <h1> 순서가 없는 리스트 </h1>
soup.find('h1').text # 텍스트 순서가 없는 리스트

# 다중요소 선택, 다중요소 리스트 리턴
soup.find_all('span')
soup.find_all('spqn')[1].text

# 반복처리
for e in soup.find_all('span'):
    print(e.text)
    
# 단일요소 선택
soup.select_one('#head').text # 텍스트 순서가 없는 리스트

# 다중요소 선택, 다중요소 리스트 리턴
soup.select(s2)[1].text

#%% BeautifulSoup 2
# requests 조항
import requests, bs4
resp = requests.get('https://finance.naver.com/')
# if resp.status_code==200:
resp.encoding
html = resp.text
# BeautifulSoup 소스는 html, 해당 소스를 파싱(parsing)
soup = bs4.BeautifulSoup(html, 'lxml')

# 주요뉴스 제목 선택자
# nth-child가 nth-of-type로 구분됨
#content > div.article > div.section > div.news_area > div > h2
s = '#content > div.article > div.section > div.news_area > div > h2'
soup.select_one(s).text

s = '#content > div.article > div.section > div.news_area > div'
soup.select(s) # 모든 li를 가지는 ul요소와 제목요소
soup.select_one(s)[0].text

#%%
# 웹브라우저에서 목록의 첫번째 요소를 선택 CSS선택자를 복사 
#:nth-child(1) 지우자
#s = '#content > div.article > div.section > div.news_area > div > ul > li:nth-child(1) > span > a'
s = '#content > div.article > div.section > div.news_area > div > ul > li > span > a'
soup.select(s) #모든li 요소 
soup.select(s)[0]
#li요소의 텍스트 
soup.select(s)[0].text

#%% 반복처리
# 주요뉴스의 탑뉴스 제목
# soup.select_one(s) # 첫번째 요소 soup.select(s)[0]

all_element = soup.select(s)
#enumerate(all_element) : (요소인덱스, 요소)들 리턴
#for문처럼 반복되는 구간에서 객체가 현재 어느 위치에 있는지 알려 주는 인덱스 값이 필요할때 
#enumerate 함수를 사용하면 매우 유용
print(enumerate(['A','B']))
#i,p 언팩킹 = (1,'A') 팩킹 
i,p = (1,'A')#[1,'A']

for i,p in enumerate(all_element):
    print(i+1,p.text)
    print('-'*30)
    
#%%
# find
soup.find('title').text
#첫 번째 태그를 추출
soup.find('a')
#모든 태그들을 한꺼번에 추출 list로 리턴
soup.find_all('a')

#첫 번째 a 태그를 추출
soup.find_all('a')[0]
#속성값 : 요소['속성명']
soup.find_all('a')[0]['href']#'#menu'
#id속성으로 요소를 추출
soup.find(id='start')

#태그명과 속성으로 요소를 추출
soup.find('div',id='start')
soup.find('div',attrs={'id':'start'})
soup.find('div',attrs={'class':'blind'})

soup('a') #soup.find_all('a')
soup('title')#soup.find('title')

#%%
#네이버 시장지표의 주요뉴스제목 10개를 출력한다.(출력형식은 임의로 한다)
# https://finance.naver.com/marketindex

import requests, bs4
url = 'https://finance.naver.com/marketindex'
resp = requests.get(url)
html = resp.text
bs = bs4.BeautifulSoup(html, 'html.parser')
## 제목과 일시 포함
## <a>(제목만) 포함
## :nth-child(n) 빼자
s = '#content > div.section_news > div > ul > li > p > a'
main_news = bs.select(s) #모든li 요소 
main_news
print('메인뉴스 개수 =',len(main_news))
for i,p in enumerate(main_news):
    print(i+1,p.text)
    print('-'*30)

#%% 응답그림파일 저장
resp = requests.get("https://blogimgs.pstatic.net/nblog/mylog/post/og_default_image_160610.png")
#response.content이미지 데이터를 가지고 파일에다(f) 데이터를 씀(write)
with open('naver_blog_logo.png', 'wb') as f:
    f.write(resp.content) #바이너리 resp.content

import urllib.request as req
url='https://movie-phinf.pstatic.net/20200518_1/15897821674803Ytys_JPEG/movie_image.jpg'
req.urlretrieve(url ,'movie_image2.jpg') # 파일 저장 

#%% naver 영화랭킹
#영화제목과 상세정보링크
import urllib.request as req
import bs4

url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20220328'
resp=req.urlopen(url)
html = resp.read()
resp.close()
html.decode()
resp.getheader('content-type')

bs= bs4.BeautifulSoup(html,'html.parser')

s = '#old_content > table > tbody > tr > td.title > div > a'
bs.select(s)[0]
main_movie = bs.select(s)
#도메인네임
addr = 'https://movie.naver.com'
for i,movie in enumerate(main_movie):
    #상세정보링크 = 도메인네임 + 경로 
    link = addr+movie['href']
    print(f'{i+1}. {movie.text} {link}') #f'{변수}'
    print('-'*50) 
    
# csv 파일저장
# csv 모듈 
import csv
#newline='' 개행 두번을 한번으로 해결
f=open('naver_movie.csv','w',encoding='utf-8',newline='')
help(open)
cw = csv.writer(f)#csv writer 객체 생성
#writerow(행튜플)
#제목행(header) 파일에 출력
cw.writerow(('영화제목','상세정보링크'))
#cw.writerow(['영화제목','상세정보링크']) #가능
for i,movie in enumerate(main_movie):
    #상세정보링크 = 도메인네임 + 경로 
    link = addr+movie['href']
    cw.writerow((movie.text,link)) 
    
f.close()

'''
주소분석
https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20220723

https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cnt&tg=0&date=20220722

요소분석
규칙성(패턴)
<div class="tit3">						
#old_content > table > tbody > tr:nth-child(2) > td.title > div > a

<div class="tit3">	
#old_content > table > tbody > tr:nth-child(3) > td.title > div > a

<div class="tit3">	
#old_content > table > tbody > tr:nth-child(55) > td.title > div > a
'''

#%% 
# zip() : 동일한 개수로 이루어진 자료형을 묶어 주는 역할을 하는 함수
list(zip([1, 2, 3], [4, 5, 6])) # [(1,4),(2,5),(3,6)]
# for in 여러개 반복(이터러블) 객체
# 여러개 반복(이터러블) 객체에 대해서 동시에 일괄 작업
for m,n in zip([1, 2, 3], [4, 5, 6]): # m,n = (1,4)
    print(m,n)

#%% 영화제목과 평점 , 상세정보링크 순으로 출력
# https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur&date=20220723
import urllib.request as req
import bs4
#자동 response.close() #연결닫기(끊기) 
with req.urlopen('https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20220329') as response: 
    html = response.read()
    bs= bs4.BeautifulSoup(html,'html.parser')
    #영화명
    main_movie_name=bs.select('#old_content > table > tbody > tr > td.title > div > a')    
    print('메인영화개수 =',len(main_movie_name))
    for i, elem in enumerate(main_movie_name) :                   
        print(f'{i+1}. {elem.string}')
        print('-'*50)
    #영화상세정보링크    
    for i, elem in enumerate(main_movie_name) :
        #link=elem['href']           
        link=elem.get('href','#')
        print(f'{i+1}. {link}')
        print('-'*50) 
     #평점     
    main_movie_point=bs.select('#old_content > table > tbody > tr > td.point')  
    for i, elem in enumerate(main_movie_point) :                   
        print(f'{i+1}. {elem.text}')
        print('-'*50)
    
    # (영화명,평점) 아이템 구성 사전 #영화제목이 키값, 평점이 벨류값(단일값)
    movie_dict={}    
    for i in range(0,len(main_movie_name)):
       movie_dict[main_movie_name[i].text] = main_movie_point[i].text 
    print(movie_dict)

#%% 영화명의 중복때문에 대신에 순위번호 i+1 혹은 순서번호 i가 키값이 되는 사전
# 벨류값(다중값)
for i in range(0,len(main_movie_name)):
    # (i,[영화명, 평점]) 아이템을 사전에 추가
   movie_dict[i] = [main_movie_name[i].text,  main_movie_point[i].text]
print(movie_dict)

#영화제목 , 평점 , 상세정보링크 출력
#for in 여러개 이터러블 객체
for movie_name,movie_point in zip(main_movie_name,main_movie_point):
    link=addr+movie_name['href']#a요소의 href 속성
    print(f'{movie_name.text} / {movie_point.text}\n상세정보링크:{link}')    
    print('-'*70) 

#%% 영화명, 평점 리스트 및 사전 객체를 pickle로 파일에 저장

# 사전 파일 저장
import pickle
f = open('movie.dat', 'wb')
pickle.dump(movie_dict, f)
f.close()

# 영어사전 뷰어
import pickle
f = open('movie.dat', 'rb')
data = pickle.load(f)
print(data)
f.close()

#%% 효율적인 집계분석 영화명, 평점 컬럼을 갖는 DataFrame을 생성
# 사전의 아이템이 DataFrame의 컬럼으로 변환
# 키값이 컬럼명
# movie_dict를 {영화명:[영화명],평점:[평점]}
movie_dict = {"영화명":[i.text for i in main_movie_name],
              "평점": [i.text for i in main_movie_point]}

# (영화명, 평점 컬럼명은 name, point로 변경)
import pandas as pd
movie_df = pd.DataFrame(movie_dict)
movie_df.columns=['name','point']

# 집계분석
movie_df.info()
movie_df.describe()
# 모든 영화평점 합, 평균
# ['point'] 자료형 object
movie_df['point'].sum() # ''+''=''
movie_df.info()
# ['point'] 자료형 float
movie_df['point'] = movie_df['point'].astype(float)
movie_df['point'].isnull().sum
movie_df['point'].isna().sum
movie_df['point'].sum()
movie_df['point'].mean()
type(movie_df.describe())
movie_df.describe().loc['mean']

# 영화명 벼로 그룹별 집계분석
# 행인덱스 name이고 집계시 name으로 정렬
movie_pivot = pd.pivot_table(data=movie_df, index=['name'])

# 평점이 가장 높은 1 ~ 5위 영화 구하기
movie_sort = movie_pivot.sort_values(by='point', ascending=False)
movie_sort.head()
movie_sort.head().reset_index()

# plt로 movie_pivot의 라인플롯 시각화
import matplotlib.pyplot as plt
plt.rc('font',family='Malgun Gothic')
plt.figure(figsize=(20,10))
plt.plot(movie_pivot) # x축이 name 행인덱스
plt.xticks(rotation=90)
plt.grid()

# 평점이 가장 높은 1 ~ 5위 영화의 라인플롯 시각화
# DataFrame의 내장 플롯 사용
movie_sort.head().plot(grid=True)

# 평점이 가장 높은 1 ~ 5위 영화의 막플롯 시각화
movie_sort.head().plot(kind= 'bar',grid=True)

#%% 
'''
quiz
1. 2019년 7월 평점이 가장 높은 1 - 5위 영화 구하기
              name  point
0              알라딘  47.30
1       어벤져스: 엔드게임  46.95
2           살인의 추억  46.90
3             교회오빠  46.49
4  뽀로로 극장판 보물섬 대모험  46.45

2. 7월 날짜별 평점이 가장 높은 1 - 5위 영화 평점의 변화를 그래프로 그리기
'''
#7월1일에서 31일 생성
pd.date_range('2019-7-1',periods=31,freq='D')

import urllib
import bs4
import pandas as pd
import matplotlib.pyplot as plt

#7월1일에서 31일 생성
date1=pd.date_range('2019-7-1',periods=31,freq='D')
movie_date=[]
movie_name=[]
movie_point=[]

for today in date1:
    html='https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cur&date={d}'
    response = urllib.request.urlopen(
            html.format(d=today.strftime('%Y%m%d')))
    #today = today.strftime('%m%d')
    #html = response.read()
    #bs=html형식으로 해석 정제된 html 내용
    #bs= bs4.BeautifulSoup(html,'html.parser')
    bs= bs4.BeautifulSoup(response,'html.parser')
    #bs:요소 찾기
    #영화명 (CSS선택자)
    main_movie_name=bs.select('#old_content > table > tbody > tr > td.title > div > a')
    # 평점
    main_movie_point=bs.select('#old_content > table > tbody > tr > td.point')
    end = len(main_movie_point)#영화개수
    #영화개수만큼 날짜 ,영화명,평점 리스트를 각 통합리스트에 확장추가
    movie_date.extend([today for n in range(0,end)])
    movie_name.extend([main_movie_name[n].text for n in range(0,end)])
    movie_point.extend([main_movie_point[n].text for n in range(0,end)])

#날짜 ,영화명,평점 사전
movie_dict = {'date':movie_date,'name':movie_name,'point':movie_point}    
movie_dict
#날짜 ,영화명,평점 DataFrame
movie_07 =pd.DataFrame(movie_dict)
movie_07
#%% 집계
#모든 영화평점 합 
movie_07['point'].sum()
#DataFrame,Series내 문자열을 숫자형으로 변환(type cast, convert)
#movie_07['point']= pd.to_numeric(movie_07['point'])
movie_07['point']=movie_07['point'].astype(float)
movie_07['point'].sum()

#영화별 평점 합
movie_pivot= pd.pivot_table(data=movie_07,index=['name'],aggfunc='sum')
movie_sort=movie_pivot.sort_values(by='point',ascending=False)
movie_sort.head()

#2019년 7월 평점이 가장 높은 1 - 5위 영화 구하기
top_5=movie_sort.head().reset_index()

#날짜별 영화 평균평점 
movie_pivot= pd.pivot_table(data=movie_07,index=['date']
,columns=['name'],values=['point'],fill_value=0)
#복합 열인덱스
movie_pivot.columns
# 복합열인덱스에서 0계층 point 열명 제거
movie_pivot.columns= movie_pivot.columns.droplevel(level=0)

#%% 시각화
top_5_name=[] #영화명리스트
for i in range(5):
    #top_5_name.append(top_5['name'][i])
    top_5_name.append(top_5.loc[i,'name'])

top_5_name

plt.rc('font',family='Malgun Gothic')
plt.figure(figsize=(20,10))
plt.plot(movie_pivot[top_5_name])
plt.legend(top_5_name,loc=3)
plt.grid()

#movie_pivot[top_5_name].plot(grid=True,figsize=(20,10))
