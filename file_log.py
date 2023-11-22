import os
import datetime

def log_file_access(root_dir):
    print('File Access Log - {}'.format(datetime.datetime.now()))
    print('-' * 50)
    
    # 파일들에 대한 정보를 저장할 리스트
    file_info_list = []

    for foldername, subfolders, filenames in os.walk(root_dir):
        for filename in filenames:
            file_path = os.path.join(foldername, filename)
            try:
                # 파일에 접근 시간 임포트
                access_time = os.path.getatime(file_path)
                
                # 파일 경로와 접근 시간을 리스트에 추가
                file_info_list.append((file_path, datetime.datetime.fromtimestamp(access_time)))
                
            except (PermissionError, FileNotFoundError, OSError) as e:
                # 액세스 거부된 파일이나 파일이 없는 경우, 시스템에서 파일에 액세스할 수 없는 경우는 무시
                pass
            except Exception as e:
                print('Error accessing {}: {}'.format(file_path, str(e)))

    # 날짜 기준으로 파일들을 정렬
    file_info_list.sort(key=lambda x: x[1], reverse=True)  # 최근에 접근한 것이 앞에 오도록 정렬

    # 20개 항목만 출력하나 상의 후 출력 개수 수정할 필요 있음
    for file_info in file_info_list[:20]:
        print('{} - {}'.format(file_info[0], file_info[1]))

if __name__ == "__main__":
    # 대상 디렉토리 개별 지정
    target_directory = r'C:'
    
    # 파일 접근 기록을 생성하고 콘솔에 출력합니다.
    log_file_access(target_directory)

    print("File access log generated successfully.")
