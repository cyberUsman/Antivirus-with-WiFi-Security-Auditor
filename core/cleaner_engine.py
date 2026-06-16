import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db_manager

def get_temp_directory():
    temp_dir = os.environ.get('TEMP') or os.environ.get('TMP')
    if not temp_dir:
        temp_dir = os.path.expanduser(r'~\AppData\Local\Temp')
    return temp_dir

def scan_junk():
    temp_dir = get_temp_directory()
    if not os.path.exists(temp_dir):
        return 0, 0, 0
        
    total_files = 0
    total_folders = 0
    total_bytes = 0
    
    for root, dirs, files in os.walk(temp_dir):
        for d in dirs:
            total_folders += 1
        for f in files:
            file_path = os.path.join(root, f)
            try:
                total_bytes += os.path.getsize(file_path)
                total_files += 1
            except (FileNotFoundError, PermissionError):
                continue
                
    return total_files, total_folders, total_bytes

def clean_junk(progress_callback=None, cancel_event=None):
    temp_dir = get_temp_directory()
    if not os.path.exists(temp_dir):
        return 0, 0
        
    deleted_count = 0
    freed_bytes = 0
    
    try:
        items = os.listdir(temp_dir)
    except PermissionError:
        return 0, 0

    for item in items:
        if cancel_event and cancel_event.is_set():
            break
            
        item_path = os.path.join(temp_dir, item)
        item_size = 0
        
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                item_size = os.path.getsize(item_path)
            elif os.path.isdir(item_path):
                for root, dirs, files in os.walk(item_path):
                    for f in files:
                        f_path = os.path.join(root, f)
                        try:
                            item_size += os.path.getsize(f_path)
                        except (PermissionError, FileNotFoundError):
                            pass
        except (PermissionError, FileNotFoundError):
            pass
            
        deleted = False
        try:
            if os.path.isfile(item_path) or os.path.islink(item_path):
                os.unlink(item_path)
                deleted = True
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                deleted = True
        except (PermissionError, FileNotFoundError, OSError):
            pass
            
        if deleted:
            deleted_count += 1
            freed_bytes += item_size
            if progress_callback:
                progress_callback(item, deleted_count, freed_bytes)

    db_manager.log_cleaner_run(deleted_count, freed_bytes)
    
    return deleted_count, freed_bytes
