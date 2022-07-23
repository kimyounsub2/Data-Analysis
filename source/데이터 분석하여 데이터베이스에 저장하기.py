#%% Lending Club Loan dataset 분석하기
#대출상품의 기간(term)에 따른 대출 총액 알아내기
# -------------------------
# loan_amnt: 대출자의 대출 총액
# loan_status: 대출의 현재 상태
# grade: LC assigned loan grade 
# int_rate: 대출 이자율
# term: 대출 상품의 기간 (36-month vs. 60-month)

# -------------------------
# 목적 : 기간별 대출 총액 출력
# 결과 대출 총액
# 입력: 기간,대출자의 대출액
# -------------------------------------
import pandas as pd
loan = pd.read_csv('C:/Users/A/Desktop/youn/python_day4/data/loan.csv')
loan.info()
loan.head()
loan.tail()
loan.describe()

# 필요한	열 발췌	및 결측값 제거하기
loan2 = loan[["loan_amnt", "loan_status", "grade", "int_rate", "term"]]

loan2.info() #현재 NaN 포함하는 행은 미존재
#loan_status열이 NaN 포함하는 행 추출 
loan2.loc[loan2["loan_status"].isnull(),:]
loan2.loc[loan2["grade"].isnull(),:]
loan2.loc[loan2["int_rate"].isnull(),:]
loan2.loc[loan2["term"].isnull(),:]
loan2.loc[loan2["loan_amnt"].isna(),:]

loan2 = loan2.dropna(how="any")
loan2
# 기간별 대출 총액 결과변수
term_to_loan_amnt_dict = {} # 중간결과변수(사전)
term_to_loan_amnt=None # 최종결과변수(Series)

# term이 가지는 값의 목록 추출
unique_terms = loan2["term"].unique()
unique_terms
# 대출상품의 기간(term)에 따른 대출 총액을 결과변수(사전)에 추가
for term in unique_terms:
   loan_amnt_sum = loan2.loc[loan2["term"]==term, "loan_amnt"].sum()
   term_to_loan_amnt_dict[term] = loan_amnt_sum 
   
term_to_loan_amnt_dict
#사전을 Series로 변환 
#키값이 행인덱스  
term_to_loan_amnt = pd.Series(term_to_loan_amnt_dict)
term_to_loan_amnt

# term_to_loan_amnt 구하기 개선 groupby()기반
# 그룹칼럼은 term , 집계칼럼은 loan_amnt, 집계방식 합계
term_to_loan_amnt1 = loan2.groupby('term')['loan_amnt'].sum
term_to_loan_amnt1

#%% 대출 상태가 불량인 사람들의 대출 등급 현황을 알아내기 

# 1. loan_status가 가지는 값의 목록 추출
# array
total_status_category = loan2["loan_status"].unique()
total_status_category
'''
Charged Off   체납
In Grace Period 유예 기간 
Fully Paid   완납
Late 지연
'''
# 2. loan_status가 불량인 인덱스 목록[1, 3, 4, 5, 6, 8] 만 선택 값추출
bad_status_category = total_status_category[[1, 3, 4, 5, 6, 8]]
bad_status_category

# loan_status 목록중의 불량/우량 여부 부울린 배열
# 불량 True / 불량 False
loan2["bad_loan_status"] = loan2["loan_status"].isin(bad_status_category)
type(loan2["bad_loan_status"])

# 3. loan_status가 불량인 사람(행)들 
# 부울린 인덱스 배열
loan2.loc[loan2['bad_loan_status'] == True]

# 4. loan_status가 불량인 사람(행)들 대추 등급 현황 파악
# 대출 등급 분포 파악(grade가 헹인덱스)
#bad_loan_status_to_grades = loan2.loc[loan2["bad_loan_status"] == True, "grade"].value_counts()
# value_counts(): 값별계수(도수분포)
# 행 인덱스 = 등급, 컬럼 = 개수
bad_loan_status_to_grades = loan2.loc[loan2["bad_loan_status"], "grade"].value_counts()
bad_loan_status_to_grades
# 행 인덱스로 행 정렬(화면배치 변경)
bad_loan_status_to_grades.sort_index()

# 5. 대출 상태가 불량인 사람들의 대출 등급 현황율 csv 파일로 저장
bad_loan_status_to_grades.to_csv("C:/Users/A/Desktop/youn/python_day4/bad_loan_status.csv", sep=",")

# 6. 대출 이자율과 대출 총액 간의 상관관계
# 0.0145
loan2["loan_amnt"].corr(loan2["int_rate"])

#%% bad_loan_status_to_gradess의 인덱스와 개수를 테이블로 저장

file = bad_loan_status_to_grades.reset_index()
file.columns=['grade','count']

import cx_Oracle as oci

# sqlalchemy
from sqlalchemy import create_engine    

# Oracle 서버와 연결(Connection 맺기) 
conn = oci.connect('hr','hr','localhost:1521/xe')

# 접속후 engine 생성
engine = create_engine('oracle+cx_oracle://hr:hr@localhost:1521/xe')

# bad_loan 테이블에 테이터를 저장 
file.to_sql('bad_loan',
          engine,
          index=False) 
pd.read_sql_query('select * from bad_loan', engine)

# 데이터베이스 emp_df 테이블에 데이터를 저장 / 강사님 답
bad_loan_status_to_grades.rename('count').reset_index().to_sql('bad_loan_df', engine , index=False) 

#%% 히스토 그램
import matplotlib.pyplot as plt
plt.hist(loan2.loc[loan2["bad_loan_status"], "grade"])
plt.grid()

loan2.loc[loan2['bad_loan_status'],'grade'].hist()
# 행 인덱스(등급)로 행 정렬(화면배치 변경)
bad_loan_status_to_grades.sort_index()

import seaborn as sns
sns.histplot(x=loan2.loc[loan2['bad_loan_status'],'grade'])
plt.grid()

#%% implot, regplot(스캐터 + 회귀분석 표현)
import seaborn as sns
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')

tips = sns.load_dataset("tips")#팁 데이터
# pip install --upgrade seaborn
#등고선 스타일
#면적이 좁으면 경사가 가파르고 두 열값간의 상관관계가 높다 
sns.kdeplot(x="total_bill", y="tip",data=tips)
plt.title("흡연여부별 식사대금에 따른 팁금액의 변동량")
#등고선 스타일
sns.jointplot(x="total_bill", y="tip",data=tips, kind="kde")

# total_bill과 tip 간 선형관계(스캐터 + 회귀직선)
sns.regplot(x='total_bill',y='tip',data=tips)
plt.title("식사대금에 따른 팁금액의 회귀 분포 변동량")

# import은 hue 그룹화 지원
# total_bill과 tip간 선형관계(스케터 + 회귀직선)
sns.lmplot(x='total_bill',y='tip',hue='smoker',data=tips)
plt.title("식사대금에 따른 팁금액의 회귀 분포 변동량")

#%% scatter plot
# x의 y의 상관 관계 확인
sns.scatterplot(x='total_bill',y='tip',data=tips)
plt.title("식사대금에 따른 팁금액")

sns.scatterplot(x='total_bill',y='tip', hue='sex',data=tips)
plt.title("성별 식사대금에 따른 팁금액")

#버블차트(값(버블)의 크기를 다르게하여 산점) 
sns.scatterplot(x="total_bill", y="tip", hue='sex',data=tips,
                size = "tip",legend = True, sizes = (20, 400),
                alpha=0.5)
plt.title("성별 식사대금에 따른 팁금액")

#%% pairplot
# x의 y의 상관 관계 확인하기 위한 기초플롯으로 널리 사용
# 각 숫자형 컬럼(열)들의 모든 상관 관계를 동시에 출력
# 모든 열간 값들의 조합 산점도(상관행렬)
# 스케터 + 히스토그램
sns.pairplot(tips)
# 회귀선 포함
sns.pairplot(tips, kind='reg')

# tip, total_bill 열의 상관 관계 출력
sns.pairplot(tips, vars=['tip','total_bill'])

#%%히스토그램(도수분포도)
#x축은 구간계급,  y축은 구간도수
#구간별 도수
sns.histplot(x="total_bill",data=tips)
plt.title("식사대금 도수분포")

#5개 구간
sns.histplot(x="total_bill",data=tips,bins=5)
plt.title("식사대금 도수분포")

#커널 밀도(kernel density) 추정 적용
#kde 곡선이 왼쪽으로 치우친 모양을 확인
sns.histplot(x="total_bill",data=tips,kde=True)
plt.title("식사대금 도수분포")

#%% 도수
# y축은 커널 밀도(kernel density) 추정으로 정규화된 수치 
sns.distplot(x="total_bill",data=tips) #오류
sns.distplot(x=tips["total_bill"])
sns.distplot(x=tips.loc[:,"total_bill"])
plt.title("식사대금 밀도분포")


