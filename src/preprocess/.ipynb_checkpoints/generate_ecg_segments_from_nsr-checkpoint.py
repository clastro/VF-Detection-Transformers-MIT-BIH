import wfdb
import numpy as np
import os
import random

# ECG 데이터와 주석 파일 로드
file_path = '/smc_work/home/weladmin/Desktop/code/Research/shea/VF/data/nsr_db_number.txt'
data_path = '/smc_work/home/weladmin/Desktop/code/Research/shea/VF/data/mit-bih-normal-sinus-rhythm-database-1.0.0/'
save_path = '/smc_work/datanvme/VF/normal/'

# 시간 문자열을 초로 변환하는 함수
def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def standardize_data(data):
    mean = np.mean(data)
    std = np.std(data)
    if std > 0:
        return (data - mean) / std
    else:
        return data - mean  # 표준편차가 0이면 평균만 빼줍니다.

def split_and_save_data(data, db_number, sample_duration, save_path):
    
    data = standardize_data(data)
    
    # 데이터 길이와 샘플 수 계산
    num_samples = len(data) // sample_duration
    
    # 데이터 블록 나누기
    blocks = [data[i*sample_duration:(i+1)*sample_duration] for i in range(num_samples)]
    
    # 랜덤으로 블록 샘플링
    selected_blocks = random.sample(blocks, k=max(300, len(blocks)))
    
    # 데이터 저장
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    for i, block in enumerate(selected_blocks):
        np.save(os.path.join(save_path, f'{db_number}_block_{i}.npy'), block)

def process_data(db_number, data_path, save_path):
    # 데이터 로드
    record = wfdb.rdrecord(data_path + db_number)
    fs = record.fs

    # 20초 간격으로 샘플 번호 계산
    samples_20sec = 20 * fs
    
    # ECG 데이터 추출
    data = record.p_signal
    
    split_and_save_data(data, f'db{db_number}', samples_20sec, save_path)

def process_all_data(file_path, data_path, save_path):
    with open(file_path, 'r') as file:
        db_numbers = [line.strip() for line in file.readlines() if line.strip()]
    
    for db_number in db_numbers:
        print(f'Processing db_{db_number}...')
        db_save_path = os.path.join(save_path, f'db_{db_number}')
        process_data(db_number, data_path, db_save_path)