'''
전국초등학교의 지역,학교명,학급수,학생수,교사수
최대 학급수의 초등학교,최대 학생수의 초등학교,최대 교사수의 초등학교 출력

최대 학급수의 초등학교 : 서울신정초등학교, 학급수 : 75개 
최대 학생수의 초등학교 : 탄벌초등학교, 학생수 : 2178명
최대 교사수의 초등학교 : 서울신정초등학교, 교사수 : 91명

복잡한 for 같은 제어로직은 넘파이로에게 맡기고 탐색,통계분석 로직에 좀 더 집중 
'''
import numpy as np
list_data = np.loadtxt('C:/Users/A/Desktop/youn/data/school_2019.csv',delimiter=',',
                  dtype=np.str_, encoding='utf-8',
                  skiprows=1)
#대략적인 정성적 구조적 분석 
#전국초등학교의 지역,학교명,학급수,학생수,교사수
list_data.shape#(6264, 5)
np.shape(list_data)

#5개 추출 확인
list_data[:5,:]

# 결측치 존재 여부
np.count_nonzero(np.isnan(list_data)) #TypeError가발생하여 형변환 아래의 방식으로  형변환

#2,3,4열선택과 형변환
data= list_data[:,2:].astype(np.int64)
np.count_nonzero(np.isnan(data)) 
#최대 학급수 요소의 인덱스,
# 최대 학생수 요소의 인덱스,
# 최대 교사수 요소의 인덱스
#통계집계에서는 axis=0 세로(행)방향=열별  
#최대 학급수 요소의 인덱스
max_index = np.argmax(data, axis=0)#array([ 138, 1999,  138], dtype=int64)

max_class = list_data[max_index[0],1]#최대 학급수인덱스의 해당 학교이름
num_class = list_data[max_index[0],2]#최대 학급수인덱스의 해당 학급수

max_student=list_data[max_index[1],1]#최대 학생수의 학교명
num_student=list_data[max_index[1],3]#최대 학생수의 학생수

max_teacher=list_data[max_index[2],1]#최대 교사수의 학교명
num_teacher=list_data[max_index[2],4]#최대 교사수의 교사수

#형식화된 화면의 콘솔 출력
print('최대 학급수의 초등학교 : %s, 학급수 : %s개 ' % (max_class, num_class))
print('최대 학생수의 초등학교 : %s, 학생수 : %s명' % (max_student, num_student))
print('최대 교사수의 초등학교 : %s, 교사수 : %s명' % (max_teacher, num_teacher))


#%%
"""
학급당 학생수(학생수 /  학급수)와 교사1인당 학생수(학생수 /  교사수)를 출력한다.
단 / 는 나눗셈을 의미하고 학급당 학생수, 교사 1인당 학생수를 
원배열의 2열과 4열에 삽입하여 배열을 출력한다.
"""
# 내가한거
import numpy as np
list_data = np.loadtxt('C:/Users/A/Desktop/youn/data/school_2019.csv',delimiter=',',
                  dtype=np.str_, encoding='utf-8',
                  skiprows=1)
list_data
data= list_data[:,2:].astype(np.int64)
np.count_nonzero(np.isnan(data))

students_per_class = np.round(data[:,1] / data[:,0])
students_per_teacher = np.around(data[:,1] / data[:,2])
list_data1 = np.insert(list_data,2,students_per_class,axis=1)
list_data2 = np.insert(list_data1,4,students_per_teacher,axis=1)
list_data2

################################################
# 답안
import numpy as np
list_data = np.loadtxt('C:/Users/A/Desktop/youn/data/school_2019.csv',delimiter=',',
                  dtype=np.str_, encoding='utf-8',
                  skiprows=1)

np.shape(list_data)

data= list_data[:,2:].astype(np.int32)
# 삽입으로 인해서 배열의 인덱스 구조가 변경
#학급당 학생수에 대한 2열 추가(모든 행값은 0으로 초기화)
data =np.insert(data,2,0,axis=1)
#교사 1인당 학생수에 대한 4열 추가(모든 행값은 0으로 초기화)
data =np.insert(data,4,0,axis=1)

#학급당 학생수 =학생수 /  학급수
#학급당 학생수  결과를 해당열에 대입
#학생수 /  학급수 결과가 정수형으로 변환
#소수자리가 절삭되므로 반올림 처리 
data[:,2]=np.round(data[:,1]/data[:,0])

#교사당 학생수 =학생수 /  교사수 결과를 해당열에 대입
# 교사수 인덱스 번호가 2에서 3으로 변경
data[:,4]=np.around(data[:,1]/data[:,3])
data

'''
학급당 학생수의 평균과 과밀학급인 행을 출력한다.
학급당 학생수 30인 이상
'''
#1. data 배열의 과밀학급 행
overcrowd_class= data[data[:,2] >=30]
#과밀학급 행수
len(data[data[:,2] >=30]) #94
#data[data[:,2] >=30].shape[0] 

#2. list_data 배열의 과밀학급 행
cond_expr =  data[:,2]>=30
#과밀학급 행 index배열 
#인덱스 배열이 포함된 튜플이 반환
np.where(cond_expr)
# 튜플의 첫번째 요소(인덱스 배열)추출
np.where(cond_expr)[0] 
len(np.where(cond_expr)[0])

#과밀학급 학교 행의 모든 정보
#인덱스집합이 리스트 혹은 배열 가능
#list_data[np.array([0,2])]
list_data[np.where(cond_expr)[0]]
#과밀학급 학교이름
list_data[np.where(cond_expr)[0],1]

#학급당 학생수의 평균,분포
m = np.round(np.mean(data[:,2]))
s= np.round(np.std(data[:,2]))

