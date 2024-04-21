import csv
import pandas as pd
import matplotlib.pyplot as plt

# 각 년도의 CRASH.csv 파일 경로
file_paths = ['./crashData_2019/CRASH.csv', './crashData_2020/CRASH.csv', './crashData_2021/CRASH.csv', './crashData_2022/CRASH.csv']
# 각 년도의 CAUSE.csv 파일 경로
cause_file_paths = ['./crashData_2019/CAUSE.csv', './crashData_2020/CAUSE.csv', './crashData_2021/CAUSE.csv', './crashData_2022/CAUSE.csv']

# 각 연도의 데이터를 저장할 딕셔너리
yearly_data = {}

# 각 년도의 CAUSE.csv 파일에서 원인 코드와 원인 설명을 연결하는 딕셔너리 생성
cause_description_mappings = {}
for cause_file_path in cause_file_paths:
    with open(cause_file_path, 'r') as subfile:
        csv_reader = csv.DictReader(subfile)
        cause_description_mapping = {}
        for row in csv_reader:
            cause_description_mapping[row['CAUSE_CD']] = row['CAUSE_MED_DESC']
        # 연도를 추출하여 딕셔너리에 저장
        year = cause_file_path.split('/')[-2][-4:]
        cause_description_mappings[year] = cause_description_mapping

# 각 연도별로 데이터를 수집하고 원인별 발생 횟수를 계산하여 딕셔너리에 저장
for file_path in file_paths:
    year = file_path.split('/')[-2][-4:]  # 파일 경로에서 연도 추출
    cause_counter = {}
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)
        crash_cause_1_cd_index = header.index('CRASH_CAUSE_1_CD')
        for row in csv_reader:
            crash_cause_1_cd = row[crash_cause_1_cd_index]
            if crash_cause_1_cd not in cause_counter:
                cause_counter[crash_cause_1_cd] = 0
            cause_counter[crash_cause_1_cd] += 1
    yearly_data[year] = cause_counter

# 원하는 원인에 대한 그래프 그리기
for cause in ['FAIL AVOID VEH AHEAD', 'FAILED YIELD ROW', 'IMPROPER TURN']:
    years = []
    frequencies = []
    for year, cause_description_mapping in cause_description_mappings.items():
        years.append(year)
        frequencies.append(yearly_data[year].get(cause, 0))
        plt.bar(years, frequencies, label=cause_description_mapping.get(cause, cause))


        plt.xlabel('Year')
        plt.ylabel('Frequency')
        plt.title('Crash Causes Over Years')
        plt.show()
        plt.legend()
