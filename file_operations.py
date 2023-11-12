import os
import shutil
 
def open_item(path):
    try:
        os.startfile(path)
    except Exception as e:
        print("Error:", e)

def rename_item(current_path, new_name):
    try:
        os.rename(current_path, new_name)
    except Exception as e:
        print("Error:", e)

def delete_item(path):
    try:
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)
        print(f"{path} 삭제")
    except Exception as e:
        print("Error:", e)
