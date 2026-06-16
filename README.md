# Antivirus & WiFi Security Auditor

Welcome to the Antivirus & WiFi Security Auditor. This is a comprehensive Python-based desktop application designed to protect your system from malicious files, audit your WiFi network for security vulnerabilities, and clean up unnecessary system junk.

## Features

* **File Scanner (Antivirus):** Deeply scans files and directories to detect and report potential threats or malware[cite: 2].
* **WiFi Security Auditor:** Analyzes your active WiFi connections to identify security risks and weak configurations[cite: 2].
* **System Cleaner:** Frees up valuable disk space by safely removing temporary files, cache, and system junk[cite: 2].
* **Modern GUI:** A clean and interactive dashboard built for seamless navigation between the scanner, auditor, and cleaner[cite: 2].
* **Audit Logging:** Automatically logs scan results and security events using a local SQLite database for future reference[cite: 2].

## Project Structure

The project is organized into modular components for scalability and clean code architecture[cite: 2]:

```text
Antivirus-WiFi-Auditor/
│
├── core/                  # Core logic and scanning algorithms
│   ├── cleaner_engine.py  # Logic for system junk cleaning
│   ├── file_engine.py     # Logic for file scanning/malware detection
│   └── wifi_engine.py     # Logic for WiFi security analysis
│
├── database/              # Local data storage
│   ├── db_manager.py      # SQLite database operations
│   └── security_audit.db  # Database file storing logs
│
├── gui/                   # Graphical User Interface components
│   ├── app.py             # Main application window setup
│   └── screens/           # Individual GUI views
│       ├── cleaner.py
│       ├── dashboard.py
│       ├── file_scanner.py
│       └── wifi_auditor.py
│
├── config.py              # Global configuration variables
├── main.py                # Main entry point of the application
└── README.md              # Project documentation

Getting Started
Prerequisites
Make sure you have Python 3.x installed on your system. You will also need to install the required GUI libraries (e.g., CustomTkinter/Tkinter) if you haven't already.

Installation
Clone the repository:

Bash
   git clone [https://github.com/your-username/Antivirus-with-WiFi-Security-Auditor.git](https://github.com/your-username/Antivirus-with-WiFi-Security-Auditor.git)
   cd Antivirus-with-WiFi-Security-Auditor
Run the application:
Launch the tool by executing the main script:

Bash
   python main.py
Built With
Python 3 - The core programming language.

SQLite3 - For lightweight, local database management.

Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the issues page.
