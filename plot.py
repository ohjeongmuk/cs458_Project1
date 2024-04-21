import csv
from collections import Counter
import matplotlib.pyplot as plt

# 각 년도의 CRASH.csv 파일 경로
file_paths = ['./crashData_2019/CRASH.csv', './crashData_2020/CRASH.csv', './crashData_2021/CRASH.csv', './crashData_2022/CRASH.csv']
# 각 년도의 CAUSE.csv 파일 경로
cause_file_paths = ['./crashData_2019/CAUSE.csv', './crashData_2020/CAUSE.csv', './crashData_2021/CAUSE.csv', './crashData_2022/CAUSE.csv']
# 원인 코드와 원인 설명을 연결하는 딕셔너리 생성
cause_mapping = {}
data = []
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
        
        # CAUSE_MED_DESC 개수를 세기 위한 Counter 객체 생성
        cause_counter = Counter()
        
        if i == 1: year = 2019
        elif i ==2: year = 2020
        elif i == 3: year = 2021
        else: year = 2022
        
        failed_yield_row = 0 
        too_fast_for_cond = 0
        fail_avoid_veh_ahead = 0
        follow_too_close = 0
        
        # CRASH_CAUSE_1_CD 열의 데이터들을 가져오면서 각 값을 CAUSE_MED_DESC로 변경하고 개수를 세기
        for row in csv_reader:
            crash_cause_1_cd = row[crash_cause_1_cd_index]
            if crash_cause_1_cd == '29':
                fail_avoid_veh_ahead += 1
            elif crash_cause_1_cd == '02':
                failed_yield_row += 1
            elif crash_cause_1_cd == '01':
                too_fast_for_cond += 1
            elif crash_cause_1_cd == "07":
                follow_too_close += 1
            
            
            #cause_med_desc = cause_mapping.get(crash_cause_1_cd, 'Unknown')
            #cause_counter[cause_med_desc] += 1
        
        print("failed_yield_row: ", failed_yield_row, "too_fast_for_cond: ", too_fast_for_cond, "fail_avoid_veh_ahead: ", fail_avoid_veh_ahead)
        dict = {'year': year, "failed_yield_row": failed_yield_row, "too_fast_for_cond": too_fast_for_cond, "fail_avoid_veh_ahead": fail_avoid_veh_ahead, "follow_too_close": follow_too_close}
        data.append(dict)


print(data)
data = sorted(data, key=lambda x: x['year'])
# x축 데이터: 년도
years = [entry['year'] for entry in data]
print(years)

years_sorted = sorted(years)
print(years_sorted)
# y축 데이터: 각 원소에 대한 값을 리스트로 변환
failed_yield_row = [entry['failed_yield_row'] for entry in data]
print(failed_yield_row)
too_fast_for_cond = [entry['too_fast_for_cond'] for entry in data]
fail_avoid_veh_ahead = [entry['fail_avoid_veh_ahead'] for entry in data]
follow_too_close = [entry['follow_too_close'] for entry in data]

# 선 그래프 그리기
plt.plot(years, failed_yield_row, color='red', label='failed yield row')
plt.plot(years, too_fast_for_cond, color='blue', label='Over Speed')
plt.plot(years, fail_avoid_veh_ahead, color='green', label='fail avoid vehicle ahead')
plt.plot(years, follow_too_close, color='black', label='follow too close')

# 그래프 제목과 범례 추가
plt.title('Traffic Accident Causes Over Years')
plt.xlabel('Year')
plt.ylabel('Number of Incidents')
plt.legend()

# x축 눈금 설정
plt.xticks(years)

# 그래프 출력
plt.show()
