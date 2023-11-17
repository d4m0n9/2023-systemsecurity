import os
from datetime import datetime
import pytz

def get_recent_file_access_log(path):
    # 경로 정규화
    path = os.path.abspath(path)

    try:
        # 입력된 경로가 파일인지 디렉토리인지 확인
        if os.path.isfile(path):
            # 파일일 경우 최근 액세스 시간을 가져옴
            last_access_time = get_last_access_time(path)
            print(f"파일 경로: {path}")
            print(f"최근 액세스 시간: {last_access_time}")
        elif os.path.isdir(path):
            # 디렉토리일 경우 디렉토리 내의 파일들에 대한 최근 액세스 시간 Top 10을 출력
            get_recent_access_times_in_directory(path)
        else:
            print("올바른 경로가 아닙니다.")
    except FileNotFoundError:
        print(f"파일 또는 디렉토리를 찾을 수 없습니다: {path}")
    except Exception as e:
        print(f"오류 발생: {e}")

def get_recent_access_times_in_directory(directory_path):
    # 디렉토리 내의 파일 목록을 가져옴
    file_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # 최근 액세스 시간을 저장할 리스트
    recent_access_times = []

    # 각 파일의 최근 액세스 시간을 가져옴
    for file_name in file_list:
        file_path = os.path.join(directory_path, file_name)
        last_access_time = get_last_access_time(file_path)
        recent_access_times.append((file_name, last_access_time))

    # 최근 액세스 시간이 최신순으로 정렬
    recent_access_times.sort(key=lambda x: x[1], reverse=True)

    # 최근 액세스 시간 Top 10을 출력
    print(f"디렉토리 경로: {directory_path}")
    print("최근 액세스 시간 Top 10:")
    for file_name, access_time in recent_access_times[:10]:
        print(f"{file_name}: {access_time}")

def get_last_access_time(file_path):
    # 파일의 속성을 가져옴
    file_stat = os.stat(file_path)

    # UTC에서 로컬 시간으로 변환
    kst = pytz.timezone('Asia/Seoul')
    last_access_time = datetime.utcfromtimestamp(file_stat.st_atime).replace(tzinfo=pytz.utc).astimezone(kst).strftime('%Y-%m-%d %H:%M:%S')

    return last_access_time

# 사용 예시
file_or_directory_path = input("파일 또는 디렉토리 경로를 입력하세요: ")
get_recent_file_access_log(file_or_directory_path)



#############################################################################

# 디렉토리 입력하는 경우 그 디렉토리 내 파일 액세스 기록 10개 출력
# 파일의 경우 마지막 액세스 기록 하나만 출력 << 10개로 고쳐볼 예정 근데 안 될 수도

#############################################################################
