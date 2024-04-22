import csv
from collections import Counter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# 각 년도의 CRASH.csv 파일 경로
file_paths = ['./crashData_2015/CRASH.csv', './crashData_2016/CRASH.csv', './crashData_2017/CRASH.csv', './crashData_2018/CRASH.csv', './crashData_2019/CRASH.csv', './crashData_2020/CRASH.csv', './crashData_2021/CRASH.csv', './crashData_2022/CRASH.csv']
# 각 년도의 CAUSE.csv 파일 경로
cause_file_paths = ['./crashData_2019/CAUSE.csv', './crashData_2020/CAUSE.csv', './crashData_2021/CAUSE.csv', './crashData_2022/CAUSE.csv']
locations = ['Portland', ['Beaverton', 'Tigard', 'Durham', 'Fairview', 'Gladstone', 'Gresham', 'Happy Valley', 'Hillsboro'], 'Salem']

# 원인 코드와 원인 설명을 연결하는 딕셔너리 생성
cause_mapping = {}
data = {'Portland-29': 0, 'Portland-02': 0, 'Portland-01': 0, 'Portland-07': 0, 'Salem-29': 0, 'Salem-02': 0, 'Salem-01': 0, 'Salem-07': 0, 'OutSkirts-29': 0, 'OutSkirts-02': 0, 'OutSkirts-01': 0, 'OutSkirts-07': 0 }

with open('./crashData_2020/CAUSE.csv', 'r') as subfile:
    csv_reader = csv.DictReader(subfile)
    for row in csv_reader:
        cause_mapping[row['CAUSE_CD']] = row['CAUSE_MED_DESC']

#print(cause_mapping)
year = 0
# CRASH.csv 파일 열기
for i, crash_file in enumerate(file_paths):
# CRASH.csv 파일 열기
    with open(crash_file, 'r') as file:
        # CSV 리더 객체 생성
        csv_reader = csv.reader(file)
        
        # 첫 번째 행을 읽어서 열 인덱스를 가져옴
        header = next(csv_reader)
        crash_cause_1_cd_index = header.index('CRASH_CAUSE_1_CD')
        crash_city_index = header.index('CITY_SECT_NM')
        
        # CAUSE_MED_DESC 개수를 세기 위한 Counter 객체 생성
        cause_counter = Counter()
        
        # Portland
        P_failed_yield_row = 0
        P_too_fast_for_cond = 0
        P_fail_avoid_veh_ahead = 0
        P_follow_too_close = 0
        
        # Salem 
        S_failed_yield_row = 0
        S_too_fast_for_cond = 0
        S_fail_avoid_veh_ahead = 0
        S_follow_too_close = 0
        
        # outSkirts 
        O_failed_yield_row = 0
        O_too_fast_for_cond = 0
        O_fail_avoid_veh_ahead = 0
        O_follow_too_close = 0
        
        
        # CRASH_CAUSE_1_CD 열의 데이터들을 가져오면서 각 값을 CAUSE_MED_DESC로 변경하고 개수를 세기
        for row in csv_reader:
            crash_cause_1_cd = row[crash_cause_1_cd_index]
            crash_city = row[crash_city_index]
            
            if 'Portland' in crash_city:
                if crash_cause_1_cd == '29':
                    data['Portland-29'] += 1
                elif crash_cause_1_cd == '02' :
                    data['Portland-02'] += 1
                elif crash_cause_1_cd == '01':
                    data['Portland-01'] += 1
                elif crash_cause_1_cd == "07":
                    data['Portland-07'] += 1
            elif 'Salem' in crash_city:
                if crash_cause_1_cd == '29':
                    data['Salem-29'] += 1
                elif crash_cause_1_cd == '02' :
                    data['Salem-02'] += 1
                elif crash_cause_1_cd == '01':
                    data['Salem-01'] += 1
                elif crash_cause_1_cd == "07":
                    data['Salem-07'] += 1
            elif any(city in crash_city for city in locations[1]):
                if crash_cause_1_cd == '29':
                    data['OutSkirts-29'] += 1
                elif crash_cause_1_cd == '02' :
                    data['OutSkirts-02'] += 1
                elif crash_cause_1_cd == '01':
                    data['OutSkirts-01'] += 1
                elif crash_cause_1_cd == "07":
                    data['OutSkirts-07'] += 1
            


print(data)
Portland = [ data['Portland-29'], data['Portland-02'], data['Portland-01'], data['Portland-07']]
Salem = [ data['Salem-29'], data['Salem-02'], data['Salem-01'], data['Salem-07']]
Portland_OutSkirts = [ data['OutSkirts-29'], data['OutSkirts-02'], data['OutSkirts-01'], data['OutSkirts-07']]

Portland = {
    'location': "Portland",
    'failed_yield_row': data['Portland-29'],
    'too_fast_for_cond': data['Portland-02'],
    'fail_avoid_veh_ahead': data['Portland-01'],
    'follow_too_close': data['Portland-07']
}

Salem = {
    'location': "Salem",
    'failed_yield_row': data['Salem-29'],
    'too_fast_for_cond': data['Salem-02'],
    'fail_avoid_veh_ahead': data['Salem-01'],
    'follow_too_close': data['Salem-07']
}

OutSkirts = {
    'location': "OutSkirts",
    'failed_yield_row': data['OutSkirts-29'],
    'too_fast_for_cond': data['OutSkirts-02'],
    'fail_avoid_veh_ahead': data['OutSkirts-01'],
    'follow_too_close': data['OutSkirts-07']
}

# 그래프를 그릴 항목들
categories = ['failed_yield_row', 'too_fast_for_cond', 'fail_avoid_veh_ahead', 'follow_too_close']
label_name = ['Failed Yield Row', 'Too Fast', 'Fail Avoid Vehicle Ahead', 'Follow Too Close']

# 막대그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))

# 그래프 데이터 설정
locations = [Portland['location'], Salem['location'], OutSkirts['location']]
for i, category in enumerate(categories):
    label_name = ''
    values = [Portland[category], Salem[category], OutSkirts[category]]
    if category == 'failed_yield_row':
        label_name = 'Failed Yield Row'
    elif category == 'too_fast_for_cond':
        label_name = 'Too Fast'
    elif category == 'fail_avoid_veh_ahead':
        label_name = 'Fail Avoid Vehicle Ahead'
    else:
        label_name = 'Follow Too Close'
    ax.bar([x + i * 0.15 for x in range(len(locations))], values, width=0.15, label=label_name)

# 그래프 타이틀 및 레이블 설정
ax.set_ylabel('Count')
ax.set_xlabel('Location')
ax.set_title('Crash counts by location and category')
ax.set_xticks([x + 0.25 for x in range(len(locations))])
ax.set_xticklabels(locations)
ax.legend()

plt.savefig('plot1.png')
# 그래프 출력
plt.show()