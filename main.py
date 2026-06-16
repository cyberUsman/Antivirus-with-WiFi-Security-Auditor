import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import db_manager
from gui.app import App

def main():
    print("--- ShieldGuard: Antivirus & WiFi Auditor Initializing ---")
    
    try:
        db_manager.init_db()
        print("[*] SQLite database initialized successfully.")
    except Exception as e:
        print(f"[!] Database initialization failed: {e}")
        sys.exit(1)

    print("[*] Launching CustomTkinter GUI mainloop...")
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
