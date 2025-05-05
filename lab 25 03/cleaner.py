import os
import time 
from datetime import datetime, timedelta


def cleanup_old_files(directory_path = 'C:\Users\Popalopa666\Desktop\lab 25 03\\', max_age_hours=1):
    current_time = datetime.now()
    max_age = timedelta(hours=max_age_hours)
    # max_age = timedelta(seconds=1)
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        # Check if it is path and not directory
        if os.path.isfile(file_path):
            # Get file modification datettime
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            
            # If file is older then 1 hour - delete
            if current_time - file_mtime > max_age:
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path} (created {file_mtime})")
                except Exception as e:
                    print(f"Error ocured while deleting {file_path}: {e}")
if __name__ == "__main__":
    while True:
        cleanup_old_files()
        time.sleep(3600)  # 1 час