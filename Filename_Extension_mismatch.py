import os
import mimetypes
from shutil import move

def classify_files(input_folder, output_folder):
    # 입력 폴더의 모든 파일 리스트 가져오기
    files = os.listdir(input_folder)

    # 불일치하는 확장자가 있는지 확인하는 플래그
    mismatch_found = False

    for file_name in files:
        file_path = os.path.join(input_folder, file_name)

        # 파일일 경우에만 처리
        if os.path.isfile(file_path):
            # 파일의 형식(MIME) 가져오기
            file_mime_type, _ = mimetypes.guess_type(file_path)

            # 파일의 확장자 가져오기
            _, file_extension = os.path.splitext(file_name)
            file_extension = file_extension[1:] # 점 제거

            # 형식과 확장자가 일치하지 않는 경우
            if file_mime_type and file_extension.lower() not in file_mime_type.lower():
                # 파일을 새로운 폴더로 이동
                new_path = os.path.join(output_folder, file_name)
                move(file_path, new_path)
                print(f"파일 '{file_name}'을(를) '{output_folder}'로 이동했습니다.")
                mismatch_found = True

    # 불일치하는 확장자가 없는 경우 메시지 표시
    if not mismatch_found:
        print("불일치한 확장자를 가진 파일이 없습니다.")

# 입력 폴더 경로, 분류된 파일을 이동시킬 출력 폴더 경로(변경해야함)
input_folder_path = r"C:\Users\samsung\OneDrive\바탕 화면\시스템보안 팀플"
output_folder_path = r"C:\Users\samsung\OneDrive\바탕 화면\시스템보안 팀플\test"

classify_files(input_folder_path, output_folder_path)
