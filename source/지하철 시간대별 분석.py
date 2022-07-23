# 2018년 평일 2호선 5-6시 사이 정류장별 승차수 top20 구하고 시각화한다.

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')
read = 'C:/Users/A/Desktop/youn/python_day4/data/서울교통공사_관할역별_일별_시간대별_이용인원_20181231(1-8호선).xlsx'
file = pd.read_excel(read, encoding="utf-8",header=1)
file.head()
file.columns
file.info()

file1 = file[(file['구분']=='평') & 
             (file['호선']=='2호선') & 
             (file['구분.1'] =='승차')]

file1['구분.1'].isnull().sum()

df_2ho_total = file1.groupby('역명')['05 ~ 06'].sum()
df_2ho_total
type(df_2ho_total) # Series
df_2ho_top20 = df_2ho_total.sort_values(ascending=False).head(20)
df_2ho_top20


plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(16,10))
sns.barplot(x=df_2ho_top20.index,
            y=df_2ho_top20.values) 



df_2ho_top20.sort_index(ascending=False)
file2 = file1.iloc[:,:7]
file3 = file2.sort_values(by = ['05 ~ 06'], ascending = False)
data = file3.head(n=20)
data


##### 강사님 답
#1. select 선택열
#구분열은 '평','휴'로 구성
#'호선
#5-6
#역명
#두번째 구분열은 승차 하차
#sum(5-6시)
#2. from df
#3. where 행 필터링 조건 
#평일 2호선  승차
#4. group by 역명
# 역명(정류장)별


#파일의 헤더줄 1번
df = pd.read_excel(read,header=1)
df.info()
#열선택 행필터링
df_2ho = df[ (df['구분'] == '평') &(df['호선'] == '2호선') &
            (df['구분.1'] == '승차')]

# 널개수
df_2ho['구분.1'].isnull().sum()
#4. group by 역명
#역명별
#역별 총 승차 인원수(모든 날의 승차 인원수)
#df_2ho.groupby('역명').size() X
df_2ho_total = df_2ho.groupby('역명')['05 ~ 06'].sum()
type(df_2ho_total)
#TypeError: sort_values() got an unexpected keyword argument
#Type이 Series 이고 sort_values() 단일컬럼이므로 'by' 사용 X
#df_2ho_total.sort_values(by='05 ~ 06', ascending=False).head(20)
df_2ho_top20 = df_2ho_total.sort_values(ascending=False).head(20)

#Series -> DataFrame sort_values(by) 사용가능
#df_2ho.groupby('역명')['05 ~ 06'].sum().to_frame()
#df_2ho_total = pd.DataFrame(df_2ho.groupby('역명')['05 ~ 06'].sum())

#'역명'(인덱스)으로 df_2ho_top20 정렬
df_2ho_top20.sort_index(ascending=False)

#Series 플롯
# ValueError
# sns.barplot(x=df_2ho_top20.index,y='05 ~ 06' , data=df_2ho_top20)
# Series인경우 단일컬럼이므로 columns 컬럼인덱스 x값들이 있다
plt.figure(figsize=(20,10))
sns.barplot(x=df_2ho_top20.index,
            y=df_2ho_top20.values,
            data=df_2ho_top20) 

#Series인경우 단일컬럼이므로 columns 컬럼인덱스 X 값들이 있다
df_2ho_top20.columns #AttributeError
df_2ho_top20.values

plt.rc('font', family='Malgun Gothic')
plt.figure(figsize=(16,10))
sns.barplot(x=df_2ho_top20.index,
            y=df_2ho_top20.values) 
#역명 가로 겹친다
plt.xticks(rotation=90)

# 수평(가로)막대
sns.barplot(y=df_2ho_top20.index,
            x=df_2ho_top20.values) 

#%% 2호선이면서 역명이 시청인 1월 승차수의 합계률 시각화 한다.
# 1월의 일자별로 추이를 출력
file.head()
file.info() 

month = file[file['날짜'] <= '2018-01-31']
city_hall = month[(month['호선'] == '2호선') &
                  (month['역명'] == '시청') &
                  (month['구분.1'] == '승차')]
city_hall
plt.figure(figsize=(20,4))
plt.xticks(rotation=90)
sns.pointplot(x='날짜',y='합 계',data=city_hall)

# 날짜 yyyy-mm-dd 형식화
from datetime import datetime

datetime.strftime(datetime.now(), '%Y-%m-%d')
datetime.strftime(city_hall['날짜'], '%Y-%m-%d') # 날짜가 Series형태여서 오류가 난다.

# dt: 해당컬럼 datetime 접근자로 모든 datetime 값들
city_hall['날짜'] = city_hall['날짜'].dt.strftime('%Y-%m-%d')

plt.figure(figsize=(20,4))
plt.xticks(rotation=90)
sns.pointplot(x='날짜',y='합 계',data=city_hall)
city_hall.columns[6:-1]

#%% 2018년 평일 2호선 18-19 사이 정류장별 혼잡도(새로운 업무적인 분석 집계지표)의 Top-10을 분석하여
# 바플롯한다. 
# 단 혼잡도는 시간대별 승,하차 이용객수 합을 기반한다. 
file.head()
file.info() 
file.sample(5) # 랜덤으로 5개만 볼수 있다
file.describe()
sns.pairplot(data=file, vars=['역번호','05 ~ 06'])

file1 = file[(file['구분']=='평') & 
             (file['호선']=='2호선')]

df_2ho_total = file1.groupby('역명')['18 ~ 19'].sum().to_frame()
df_2ho_total.info()
df_2ho_total.head()

df_2ho_top10 = df_2ho_total.sort_values(by='18 ~ 19',ascending=False).head(10)
df_2ho_top10


plt.figure(figsize=(16,10))
plt.xticks(rotation=90)
sns.barplot(y=df_2ho_top10.index,
            x=df_2ho_top10['18 ~ 19']) 