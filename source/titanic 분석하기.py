'''
titanic
survived 생존여부(수치) 1,0
alive 생존여부(문자) yes,no
pclass 티켓의 클래스,객실등급 1=1st, 2=2nd, 3=3rd 범주(카테고리)형 수치
class 티켓의 클래스,객실등급 범주(카테고리)형 문자
sex 성별 male, female 
age 나이 연속형 수치
sibSp 함께 탑승한 형제와 배우자의 수 
parch 함께 탑승한 부모, 아이의 수  정량형 수치
ticket 티켓 번호 
fare 탑승료 
cabin 객실 번호 
embared 탑승 항구 C=Cherbourg Q=Queenstown S=Southampton 

퀴즈
1. 전체승객을 나이별로 히스토그램으로 출력(distplot)
2. 남.여 승객수를 출력 (countplot)
3. 객실별 사망자 수를 출력 (countplot)
4. 객실별 승객수를 출력 (countplot)
5. 사망자와 생존자를 출력 (plot.pie) 
6. 남/여 성별 사망자와 생존자를 출력  (countplot)
7. 객실등급별 나이분포를 출력 (boxplot)
'''
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')

titanic = sns.load_dataset('titanic')
titanic.info()
titanic.columns
titanic.head()
titanic.describe()

# 전처리 과정
# 중복행 개수
titanic.duplicated().sum()
# 중복행 제거
titanic.drop_duplicates()
titanic['age'] = titanic['age'].dropna()

# 1 전체승객을 나이별로 히스토그램으로 출력(distplot)
sns.distplot(x=titanic.dropna()['age'])
plt.title('전체승객을 나이별로 히스토그램으로 출력')
# 전체요금 분포를 히스토그램과 커널밀도 출력(널값은 평균값으로 변환)
titanic['fare'].fillna(titanic['fare'].mean(), inplace=True)
sns.histplot(titanic['fare'])
sns.distplot(titanic['fare'])

# 2 남.여 승객수를 출력 (countplot)
sns.countplot(x='sex', data=titanic)
sns.countplot(titanic['sex'])
plt.title('남.여 승객수를 출력')

# 3 객실별 사망자 수를 출력 (countplot)
sns.countplot(x='class',hue='alive', data=titanic)
sns.lineplot(x='class',y='survived', data=titanic)
plt.title('객실별 승객수 수를 출력')

sns.countplot(x = 'class', data = titanic[titanic['survived']==0])
plt.title('Dead of Titanic by Class')
plt.xlabel('Class level')
plt.ylabel('Count')

#리턴값 axes
ax = sns.countplot(x = 'class', data = titanic[titanic['survived']==0])
ax.set_title('Dead of Titanic by Class')
plt.set_xlabel('Class level')
plt.set_ylabel('Count')

# 4 객실별 승객수를 출력 (countplot)
sns.countplot(x='class', data=titanic)
plt.title('객실별 승객수 수를 출력')

# 5
count = titanic['survived'].value_counts()
count.plot.pie(autopct = '%1.1f%%',labels=["Dead", "Survived"])

#as_index = False : 원래 그룹 컬럼이 행인덱스로 되는데  
#그룹 컬럼을 일반컬럼으로 구성하고  행인덱스는 정수인덱스로 생성 
titanic_survived = titanic.groupby(["survived"], 
                   as_index = False).count()["pclass"]
#0    549
#1    342
plt.pie(titanic_survived, labels=["Dead", "Survived"], 
        autopct='%1.1f%%', shadow=True, startangle=90)

#열.value_counts().plot.pie
titanic['survived'].value_counts().plot.pie(explode=[0, 0.1],
                                            autopct='%1.1f%%',
                                            shadow=True)
titanic['alive'].value_counts().plot.pie(explode=[0, 0.1], 
                                         autopct='%1.1f%%',
                                           shadow=True)

# 6 
sns.countplot(x='survived',hue='sex', data=titanic) # 남성이 사망이 많다
plt.title('남/여 성별 사망자와 생존자를 출력')

# 7 
sns.boxplot(x='pclass', y='age', data= titanic)
plt.title('객실등급별 나이분포를 출력')

#%%
# 히트맵
# 자료의 집계 결과를 색깔을 다르게 해서 2차원으로 시각화하는 히트맵
titanic.corr()
sns.heatmap(titanic.corr(),  annot=True)
#객실별(클래스별) 성별 구분 요금 테이블(pivot_table)
#행은 객실 ,열은 성 , 행열값은 요금평균, 집계는 평균
titanic_pt = titanic.pivot_table(index="pclass", 
                                 columns="sex",
                                 values='fare')
titanic_pt
plt.figure(figsize=(10,10))
sns.heatmap(titanic_pt ,annot=True)
#fmt='d' 정수
#fmt='.2f' 소수점 이하 2자리수 실수
sns.heatmap(titanic_pt ,fmt='.2f',annot=True)

# 객실별(클래스 class별) 
# 성별 (열이 sex) 
# 구분 승객수 테이블(pivot_table) 히트맵
# 요금의 개수(행열값)가 널값 없으므로 승객수이다 
# 집계는 개수 np.size
import numpy as np
titanic_pt = titanic.pivot_table(index="pclass", 
                                 columns="sex",
                                 values='fare',
                                 aggfunc=[np.size])

sns.heatmap(titanic_pt ,annot=True)
