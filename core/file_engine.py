import os
import hashlib
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config
from database import db_manager

def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()
    try:
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (PermissionError, FileNotFoundError, IsADirectoryError, OSError):
        return None

def scan_directory(target_path, scan_type="Full", progress_callback=None, cancel_event=None):
    files_scanned = 0
    threats_found = 0
    detected_threats = []
    
    if os.path.isfile(target_path):
        files_to_scan = [target_path]
    elif os.path.isdir(target_path):
        files_to_scan = []
        for root, dirs, files in os.walk(target_path):
            if cancel_event and cancel_event.is_set():
                break
            for file in files:
                files_to_scan.append(os.path.join(root, file))
    else:
        return 0, 0, []

    for file_path in files_to_scan:
        if cancel_event and cancel_event.is_set():
            break
            
        file_hash = calculate_sha256(file_path)
        files_scanned += 1
        threat_info = None
        
        if file_hash:
            if file_hash in config.VIRUS_SIGNATURES:
                threat_name = config.VIRUS_SIGNATURES[file_hash]
                threats_found += 1
                threat_info = (file_path, threat_name, file_hash)
                detected_threats.append(threat_info)
                
        if progress_callback:
            progress_callback(file_path, files_scanned, threats_found, threat_info)

    status = "Threats Blocked" if threats_found > 0 else "Clean"
    if cancel_event and cancel_event.is_set():
        status = "Aborted"
        
    db_manager.log_antivirus_scan(
        scan_type=scan_type,
        target_path=target_path,
        files_scanned=files_scanned,
        threats_found=threats_found,
        status=status
    )
    
    return files_scanned, threats_found, detected_threats