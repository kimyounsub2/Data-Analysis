import csv
import numpy as np
f = open('C:/Users/A/Desktop/youn/data/school_2019.csv','r',encoding='utf-8')
lines = csv.reader(f)
header = next(lines)

list_data = []
for line in lines:
    list_data.append(line[:]) 

length = len(list_data)

data = np.zeros((length, 3), dtype='int32')

for i in range(length) :
    for j in range(3) :
        data[i][j] = list_data[i][j+2]

max_index = np.argmax(data, axis=0) #열별의 최댓값 index위치
print(max_index)
    
max_class = list_data[max_index[0]][1] #최대 학급수 초등학교
num_class = list_data[max_index[0]][2] #학급수 개수

max_student = list_data[max_index[1]][1] #최대 학생수 초등학교
num_student = list_data[max_index[1]][3] #학생수 개수

max_teacher = list_data[max_index[2]][1] #최대 교사 초등학교
num_teacher = list_data[max_index[2]][4] #교사수 개수

print('최대 학급수의 초등학교 :%s, 학급 수 :%s개'%(max_class,num_class))
print('최대 학생수의 초등학교 :%s, 학생 수 :%s개'%(max_student,num_student))
print('최대 교사수의 초등학교 :%s, 교사 수 :%s개'%(max_teacher,num_teacher))

f.close
