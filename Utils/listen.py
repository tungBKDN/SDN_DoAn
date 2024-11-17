import os
import time
from datetime import datetime


def watch_file_polling(file_path):
    last_modified_time = os.path.getmtime(file_path)
    while True:
        try:
            current_modified_time = os.path.getmtime(file_path)
            if current_modified_time != last_modified_time:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print(f"{current_time}: There should be an DDoS attack, check the file at /var/log/snort/alert/alert.")
                last_modified_time = current_modified_time
            time.sleep(1)
        except FileNotFoundError:
            print(f"{file_path} not found.")
            time.sleep(1)

if __name__ == "__main__":
    watch_file_polling("/var/log/snort/alert/alert")

