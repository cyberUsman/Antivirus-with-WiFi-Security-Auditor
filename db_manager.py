import sqlite3
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import config

def get_db_connection():
    os.makedirs(config.DB_DIR, exist_ok=True)
    conn = sqlite3.connect(config.DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS antivirus_scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            scan_type TEXT NOT NULL,
            target_path TEXT NOT NULL,
            files_scanned INTEGER DEFAULT 0,
            threats_found INTEGER DEFAULT 0,
            status TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cleaner_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            files_deleted INTEGER DEFAULT 0,
            bytes_freed INTEGER DEFAULT 0
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wifi_audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            networks_found INTEGER DEFAULT 0,
            insecure_networks INTEGER DEFAULT 0,
            details TEXT
        )
    """)
    
    conn.commit()
    conn.close()

def log_antivirus_scan(scan_type, target_path, files_scanned, threats_found, status):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO antivirus_scans (scan_type, target_path, files_scanned, threats_found, status)
        VALUES (?, ?, ?, ?, ?)
    """, (scan_type, target_path, files_scanned, threats_found, status))
    conn.commit()
    conn.close()

def log_cleaner_run(files_deleted, bytes_freed):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO cleaner_history (files_deleted, bytes_freed)
        VALUES (?, ?)
    """, (files_deleted, bytes_freed))
    conn.commit()
    conn.close()

def log_wifi_audit(networks_found, insecure_networks, details_str):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wifi_audits (networks_found, insecure_networks, details)
        VALUES (?, ?, ?)
    """, (networks_found, insecure_networks, details_str))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT SUM(threats_found) FROM antivirus_scans")
    total_threats = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT SUM(files_scanned) FROM antivirus_scans")
    total_files_scanned = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT COUNT(*), SUM(bytes_freed) FROM cleaner_history")
    cleanup_count, total_bytes_freed = cursor.fetchone()
    cleanup_count = cleanup_count or 0
    total_bytes_freed = total_bytes_freed or 0
    
    cursor.execute("SELECT networks_found, insecure_networks FROM wifi_audits ORDER BY timestamp DESC LIMIT 1")
    wifi_row = cursor.fetchone()
    if wifi_row:
        last_wifi_total = wifi_row[0]
        last_wifi_insecure = wifi_row[1]
    else:
        last_wifi_total = 0
        last_wifi_insecure = 0
        
    conn.close()
    
    return {
        "total_threats": total_threats,
        "total_files_scanned": total_files_scanned,
        "cleanup_count": cleanup_count,
        "total_bytes_freed": total_bytes_freed,
        "last_wifi_total": last_wifi_total,
        "last_wifi_insecure": last_wifi_insecure
    }

def get_recent_activities(limit=5):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    activities = []
    
    cursor.execute("""
        SELECT timestamp, 'Antivirus Scan' as type, 
        'Scanned ' || files_scanned || ' files. Threats found: ' || threats_found || ' (' || status || ')' as msg 
        FROM antivirus_scans ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    for row in cursor.fetchall():
        activities.append(dict(row))
        
    cursor.execute("""
        SELECT timestamp, 'Junk Cleaner' as type, 
        'Cleaned ' || files_deleted || ' files. Freed ' || 
        CASE 
            WHEN bytes_freed > 1024 * 1024 * 1024 THEN printf('%.2f GB', bytes_freed / 1024.0 / 1024.0 / 1024.0)
            WHEN bytes_freed > 1024 * 1024 THEN printf('%.2f MB', bytes_freed / 1024.0 / 1024.0)
            WHEN bytes_freed > 1024 THEN printf('%.2f KB', bytes_freed / 1024.0)
            ELSE bytes_freed || ' Bytes'
        END as msg
        FROM cleaner_history ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    for row in cursor.fetchall():
        activities.append(dict(row))
        
    cursor.execute("""
        SELECT timestamp, 'WiFi Audit' as type, 
        'Audited ' || networks_found || ' networks. Insecure: ' || insecure_networks as msg 
        FROM wifi_audits ORDER BY timestamp DESC LIMIT ?
    """, (limit,))
    for row in cursor.fetchall():
        activities.append(dict(row))
        
    conn.close()
    
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    return activities[:limit]

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")
