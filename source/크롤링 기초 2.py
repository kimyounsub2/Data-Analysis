#%% 할리스 커피 매장 크롤링
'''
할리스커피 50개 일부 매장 정보를 크롤링해본다.
단 출력정보는 지역,매장명,주소,전화번호
https://www.hollys.co.kr/    
-> Store
'''
#프로그램 구조
#메인함수 main() + 서브함수 hollys_store()
#메인함수가 서브함수 api를 호출
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

def hollys_store(result):#result은 이차리스트
    #for i in count(): # count() : 페이지번호 무한 이터레이터 생성
    for page in range(1,6):        
        Hollys_url = 'https://www.hollys.co.kr/store/korea/korStore.do?pageNo=%d&sido=&gugun=&store=' %page
        print(Hollys_url)
        html = urllib.request.urlopen(Hollys_url)
        soupHollys = BeautifulSoup(html, 'html.parser')
        tag_tbody = soupHollys.find('tbody')
        for store in tag_tbody.find_all('tr'):
            #print('store >>>>',store)
            #print('len(store) >>>>',len(store))
            #len(store) :store 행(tr)하위요소 개수               
            if len(store) <= 3: 
                break
            store_td = store.find_all('td')
            store_name = store_td[1].text
            store_sido = store_td[0].text
            store_address = store_td[3].text
            store_phone = store_td[5].text
            # 데이터프레임에서 네개의 컬럼이 생성
            result.append([store_name]+[store_sido]+[store_address]+[store_phone])
            '''
            # 데이터 프레임에서 하나의 컬럼이 생성
            result.append([store_name + store_sido + store_address + store_phone])
            '''
    return

def main():
    res = []
    print('Hollys store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    hollys_store(res)   
    hollys_tbl = pd.DataFrame(res, 
        columns=('store', 'sido-gu', 'address','phone'))
    hollys_tbl.to_csv('hollys.csv', encoding='utf-8',
                      mode='w', index=False)
    print(res[:])
       
main()

#%% count()
from itertools import count
#0부터 시작하는 숫자 무한 생성 이터레이터 
for page in count():    
    print(page)
    if page == 100:
        break
    
#for page in count(): 
#5부터 시작하고 2씩 증가하는 숫자 무한 생성 이터레이터 
for page in count(5,2):    
    print(page)
    if page >= 10:
        break  
    
store =None;
print(store)

if(store): #store가 값이 미존재 Fasle로 해석
    print(store)
    
if not store: #True
    print(store)    

store ='할리스 서울 매장';
if store: #store가 True 해석
    print(store)

store =['할리스 서울 매장'];
if store: #store가 True 해석
    print(store)

store =[];
if store: #store가 빈리스트 Fasle로 해석
    print(store) 
'''
try:
    ...
except 발생 오류:
    ...
이 경우는 오류가 발생했을 때 except문에 미리 정해 놓은 오류 이름과 일치할 때만 except 블록을 수행한다는 뜻
'''
def hollys_store(result):#result은 이차리스트
    #for i in count(): # count() : 페이지번호 무한 이터레이터 생성
    for page in range(1,6):        
        Hollys_url = 'https://www.hollys.co.kr/store/korea/korStore.do?pageNo=%d&sido=&gugun=&store=' %page
        print(Hollys_url)
        html = urllib.request.urlopen(Hollys_url)
        soupHollys = BeautifulSoup(html, 'html.parser')
        tag_tbody = soupHollys.find('tbody')
        for store in tag_tbody.find_all('tr'):
            try:
                store_td = store.find_all('td')
                # 탈출조건 : td 인덱스 존재하지 않으면(인덱스 오류 )함수 탈출
                store_name = store_td[1].text
                store_sido = store_td[0].text
                store_address = store_td[3].text
                store_phone = store_td[5].text
                # 데이터프레임에서 네개의 컬럼이 생성
                result.append([store_name]+[store_sido]+[store_address]+[store_phone])
            '''
            # 데이터 프레임에서 하나의 컬럼이 생성
            result.append([store_name + store_sido + store_address + store_phone])
            '''
            except:
                print('더이상 매장정보가 없다')
                return # 함수 탈출

def main():
    res = []
    print('Hollys store crawling >>>>>>>>>>>>>>>>>>>>>>>>>>')
    hollys_store(res)   
    hollys_tbl = pd.DataFrame(res, 
        columns=('store', 'sido-gu', 'address','phone'))
    hollys_tbl.to_csv('hollys.csv', encoding='utf-8',
                      mode='w', index=False)
    print(res[:])
       
main()
#%%플랜트 수주 정보 크롤링
'''
http://kopia.or.kr/info/statistics.php
css 선택자 기반문제발생 시
HTML소스코드 직접확인 
'''
from bs4 import BeautifulSoup
import requests
#%%
url = "http://kopia.or.kr/info/statistics.php"
page = requests.get(url)
#%%
try:
    #잘못된 주소면 400이고 예외는 발생하지 않기때문에 
    #if else로 처리
    if page.status_code == 200:  
        soup = BeautifulSoup(page.text, 'html.parser')
        #제목 column명을 받기 위한 과정
        a = soup.find_all('th')     
        #수주데이터를 가져오는 과정        
        #크롬에서는 tbody 보이지만 HTML소스코드에서는 tbody 실제로 없음
        #b가 빈리스트
        b = soup.select('#contents > div.contentArea > div.content_in > div > div.scroll_cont > table > tbody > tr > td') # 빈리스트
        #'tbody >' 제거
        #b가 7개 td로 구성된 리스트 
        #b = soup.select('#contents > div.contentArea > div.content_in > div > div.scroll_cont > table > tr > td')
        b = soup.find_all('td')
    else:
        print(page.status_code)
        print('failed')
        
    for i in b:
        print(i)
except:
    print('failed')

#가져온 데이터 b의 text를 m_col에 넣는 과정
m_col = []
for tag in b:
    m_col.append(tag.text)
    #print(tag.text)
print(m_col)

#가져온 데이터 m_col를 각 list에 넣는 과정
m_country = [] #발주지역 및 발주국가
m_inher = [] # 수주기업
m_equip = [] # 설비구분
m_pro = [] #프로젝트 명
m_odoz = [] # 발주처
m_pay = [] #수주 금액
m_time = [] #수주 시기

#m_col의 공차 7, % 활용하여 m_col 데이터를 각 list에 넣는다
for i in range(0,len(b)):
    if i%7==0: #0,7,14번등은 발주국가로 나머지 0이다
        m_country.append(b[i].text)
    elif i%7 == 1:#1,8,15번등은 수주기업으로 나머지 1이다
        m_inher.append(b[i].text)
    elif i%7 == 2:
        m_equip.append(b[i].text)
    elif i%7 == 3:
        m_pro.append(b[i].text)
    elif i%7 == 4:
        m_odoz.append(b[i].text)
    elif i%7 == 5:
        m_pay.append(b[i].text)
    elif i%7 == 6:
        m_time.append(b[i].text)
    else:
        print("something wrong")

#상위 데이터 10개만 출력 
for i in range(0,10):
     print(m_country[i],m_inher[i],m_equip[i],m_pro[i],m_odoz[i],m_pay[i],m_time[i])    
