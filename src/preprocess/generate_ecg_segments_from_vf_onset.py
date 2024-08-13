import wfdb
import numpy as np
import os
import argparse
from scipy.signal import resample

def time_to_seconds(time_str):
    h, m, s = map(int, time_str.split(':'))
    return h * 3600 + m * 60 + s

def load_data(db_number, vf_start_time_str, data_path):
    record = wfdb.rdrecord(os.path.join(data_path, db_number))
    fs = record.fs
    annotation = wfdb.rdann(os.path.join(data_path, db_number), 'atr')  # 주석 파일 로드
    
    if vf_start_time_str is None:
        return None, None, None

    # VF 발생 시간 (초 단위로 변환)
    vf_start_time = time_to_seconds(vf_start_time_str)

    return record, fs, annotation, vf_start_time

def resample_data(data, original_fs, target_fs):
    if len(data) == 0:
        return np.array([])  # 빈 데이터 처리
    num_samples = int(len(data) * target_fs / original_fs)
    return resample(data, num_samples)

def standardize_data(data):
    if len(data) == 0:
        return np.array([])  # 빈 데이터 처리
    mean = np.mean(data)
    std = np.std(data)
    return (data - mean) / std

# 데이터 나누기 및 저장
def split_and_save_data(data, db_number, samples_20sec, save_path):
    num_segments = len(data) // samples_20sec
    os.makedirs(save_path, exist_ok=True)
    
    for i in range(num_segments):
        segment = data[i * samples_20sec:(i + 1) * samples_20sec]
        filename = os.path.join(save_path, f'{db_number}_segment_{i+1}.npy')
        np.save(filename, segment)

# 데이터 처리
def process_data(db_number, vf_start_time_str, data_path, interval_start, interval_end, save_path):
    record, fs, vf_start_time = load_data(db_number, vf_start_time_str, data_path)
    if record is not None:
        # 시간대 간격 (초 단위)
        interval_start_seconds = interval_start * 60
        interval_end_seconds = interval_end * 60

        # 20초 간격으로 샘플 번호 계산
        samples_20sec = 20 * 128  # 목표 주파수 128Hz로 설정
        
        # VF 발생 지점의 시간대 간격에 따른 샘플 번호 계산
        sample_start = vf_start_time - interval_end_seconds
        sample_end = vf_start_time - interval_start_seconds

        # ECG 데이터 추출
        data = record.p_signal[int(sample_start * fs):int(sample_end * fs) + int(20 * fs)]

        # 리샘플링
        resampled_data = resample_data(data, fs, 128)
        # 표준화
        standardized_data = standardize_data(resampled_data)
        
        split_and_save_data(standardized_data, db_number, samples_20sec, save_path)
data_path = './data/sudden-cardiac-death-holter-database-1.0.0/'
    # 데이터베이스와 VF 발생 시간 목록
databases = [
    ('30', '07:54:33'),
    ('31', '13:42:24'),
    ('32', '16:45:18'),
    ('33', '04:46:19'),
    ('34', '06:35:44'),
    ('35', '24:34:56'),
    ('36', '18:59:01'),
    ('37', '01:31:13'),
    ('38', '08:01:54'),
    ('39', '04:37:51'),
    #('40', None),  # pacing, no VF
    ('41', '02:59:24'),
    #('42', None),  # no VF
    ('43', '15:37:11'),
    ('44', '19:38:45'),
    ('45', '18:09:17'),
    ('46', '03:41:47'),
    ('47', '06:13:01'),
    ('48', '02:29:40'),
    #('49', None),  # pacing, no VF
    ('50', '11:45:43'),
    ('51', '22:58:23'),
    ('52', '02:32:40')
]

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process ECG data for VF prediction.')
    parser.add_argument('--interval_start', type=int, required=True, help='Start of the time interval in minutes')
    parser.add_argument('--interval_end', type=int, required=True, help='End of the time interval in minutes')

    args = parser.parse_args()

    save_path = f'/smc_work/datanvme/VF/vf_before_min_{args.interval_start}_{args.interval_end}/'  # 데이터 저장 경로

    # 데이터 처리 반복
    for db_number, vf_start_time_str in databases:
        if vf_start_time_str is not None:  # VF 발생 시간이 없는 데이터는 스킵
            process_data(db_number, vf_start_time_str, data_path, args.interval_start, args.interval_end, save_path)
        else:
            print(f'Skipping database {db_number} due to no VF onset time.')
