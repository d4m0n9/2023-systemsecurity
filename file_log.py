import os
from datetime import datetime
import logging.handlers

class FileAccessLogger:
    def __init__(self, log_dir, log_name):
        self.log_path = os.path.join(log_dir, f"{log_name}.log")
        self.init_logger()

    def init_logger(self):
        formatter = logging.Formatter("[%(asctime)s] %(message)s")
        file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=self.log_path, when='midnight', interval=1, backupCount=7, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)

        self.logger = logging.getLogger("FileAccessLogger")
        self.logger.addHandler(file_handler)
        self.logger.setLevel(logging.INFO)

    def log_file_access(self, file_path):
        file_access_time = datetime.fromtimestamp(os.path.getatime(file_path)).strftime("%Y-%m-%d %H:%M:%S")
        self.logger.info(f"{file_access_time} - File accessed: {file_path}")

    def view_file_access_log(self):
        try:
            with open(self.log_path, "r") as log_file:
                file_access_log = log_file.readlines()
                for log_entry in file_access_log:
                    print(log_entry.strip())
        except FileNotFoundError:
            print("파일 열람 이력이 없습니다.")


if __name__ == "__main__":
    log = FileAccessLogger(".", "test")

    # 예제로 파일 열람 기록 남기기
    file_path_to_monitor = "C:\\Users\\damong\\Desktop\\test.txt"
    log.log_file_access(file_path_to_monitor)

    # 파일 열람 이력 조회 및 출력
    log.view_file_access_log()

