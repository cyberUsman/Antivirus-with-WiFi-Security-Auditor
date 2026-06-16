import customtkinter as ctk
import os
import sys
import threading
from tkinter import filedialog

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.file_engine import scan_directory

class FileScannerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.scanning = False
        self.cancel_event = threading.Event()
        
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self, 
            text="Antivirus Scanner", 
            font=ctk.CTkFont(size=26, weight="bold", family="Segoe UI"),
            text_color="#f8fafc"
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        self.setup_path_selector()

        self.setup_progress_widgets()

        self.setup_console()

    def setup_path_selector(self):
        self.path_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.path_frame.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.path_frame.grid_columnconfigure(1, weight=1)

        self.lbl_path = ctk.CTkLabel(
            self.path_frame, 
            text="Target Directory:", 
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            text_color="#cbd5e1"
        )
        self.lbl_path.grid(row=0, column=0, padx=15, pady=15, sticky="w")

        default_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.entry_path = ctk.CTkEntry(
            self.path_frame, 
            font=ctk.CTkFont(size=12, family="Consolas"),
            fg_color="#0f172a",
            border_color="#1e293b"
        )
        self.entry_path.insert(0, default_path)
        self.entry_path.grid(row=0, column=1, padx=(0, 10), pady=15, sticky="ew")

        self.btn_browse = ctk.CTkButton(
            self.path_frame, 
            text="📁 Browse", 
            width=100,
            fg_color="#1e293b",
            text_color="#94a3b8",
            hover_color="#334155",
            command=self.browse_folder
        )
        self.btn_browse.grid(row=0, column=2, padx=(0, 10), pady=15)

        self.btn_scan = ctk.CTkButton(
            self.path_frame, 
            text="⚡ Start Scan", 
            width=120, 
            fg_color="#10b981", 
            hover_color="#059669", 
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            command=self.start_scan
        )
        self.btn_scan.grid(row=0, column=3, padx=(0, 15), pady=15)

    def setup_progress_widgets(self):
        self.progress_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.progress_frame.grid_columnconfigure(0, weight=1)

        self.lbl_current_file = ctk.CTkLabel(
            self.progress_frame, 
            text="Scanning: Initializing...", 
            font=ctk.CTkFont(size=12, family="Segoe UI"), 
            text_color="#94a3b8",
            anchor="w"
        )
        self.lbl_current_file.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="ew")

        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame, 
            orientation="horizontal",
            progress_color="#0ea5e9"
        )
        self.progress_bar.set(0)
        self.progress_bar.grid(row=1, column=0, padx=15, pady=5, sticky="ew")

        self.stats_frame = ctk.CTkFrame(self.progress_frame, fg_color="transparent")
        self.stats_frame.grid(row=2, column=0, padx=15, pady=(5, 15), sticky="ew")

        self.lbl_scan_count = ctk.CTkLabel(
            self.stats_frame, 
            text="Scanned: 0 files", 
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            text_color="#cbd5e1"
        )
        self.lbl_scan_count.pack(side="left")

        self.lbl_threats_count = ctk.CTkLabel(
            self.stats_frame, 
            text="Threats: 0", 
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"), 
            text_color="#f43f5e"
        )
        self.lbl_threats_count.pack(side="left", padx=30)

        self.btn_cancel = ctk.CTkButton(
            self.stats_frame, 
            text="🛑 Abort Scan", 
            width=110, 
            fg_color="#f43f5e", 
            hover_color="#e11d48", 
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            command=self.cancel_scan
        )
        self.btn_cancel.pack(side="right")

    def setup_console(self):
        self.console_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.console_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 5))
        self.console_frame.grid_rowconfigure(0, weight=1)
        self.console_frame.grid_columnconfigure(0, weight=1)

        self.txt_console = ctk.CTkTextbox(
            self.console_frame, 
            font=ctk.CTkFont(family="Consolas", size=11), 
            fg_color="#020617",
            border_width=0
        )
        self.txt_console.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        self.txt_console.tag_config("info", foreground="#64748b")
        self.txt_console.tag_config("success", foreground="#10b981")
        self.txt_console.tag_config("threat", foreground="#f43f5e")
        self.txt_console.tag_config("warning", foreground="#f59e0b")

        self.append_log("[INF] ShieldGuard Antivirus scanning console initialized.\n", "info")
        self.append_log("[INF] Select a path and click 'Start Scan' to trigger the checksum engine.\n", "info")

    def append_log(self, text, tag="info"):
        self.txt_console.configure(state="normal")
        self.txt_console.insert("end", text, tag)
        self.txt_console.see("end")
        self.txt_console.configure(state="disabled")

    def browse_folder(self):
        path = filedialog.askdirectory()
        if path:
            self.entry_path.delete(0, "end")
            self.entry_path.insert(0, path)

    def start_scan(self):
        if self.scanning:
            return
            
        target = self.entry_path.get()
        if not target or not os.path.exists(target):
            self.append_log(f"[ERR] Error: Target path '{target}' is invalid.\n", "threat")
            return

        self.scanning = True
        self.cancel_event.clear()
        
        self.progress_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        
        self.btn_scan.configure(state="disabled")
        self.btn_browse.configure(state="disabled")
        self.entry_path.configure(state="disabled")
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()

        self.append_log(f"[INF] Hashing signatures walkthrough initialized at path: {target}\n", "info")

        scan_thread = threading.Thread(
            target=self.run_scan_thread,
            args=(target,)
        )
        scan_thread.daemon = True
        scan_thread.start()

    def run_scan_thread(self, path):
        def callback(current_path, files_scanned, threats_found, threat_info):
            basename = os.path.basename(current_path)
            self.lbl_current_file.configure(text=f"Scanning: {basename}")
            self.lbl_scan_count.configure(text=f"Scanned: {files_scanned} files")
            self.lbl_threats_count.configure(text=f"Threats: {threats_found}")

            if threat_info:
                file_p, threat_name, f_hash = threat_info
                self.append_log(f"[THREAT] MALWARE MATCH FOUND!\n  Threat: {threat_name}\n  Path: {file_p}\n  SHA-256: {f_hash}\n", "threat")
            else:
                self.append_log(f"[OK] SHA256 matches clean DB -> {current_path}\n", "info")

        files_scanned, threats_found, detected_threats = scan_directory(
            target_path=path,
            scan_type="Full",
            progress_callback=callback,
            cancel_event=self.cancel_event
        )

        self.after(0, lambda: self.finish_scan(files_scanned, threats_found, detected_threats))

    def finish_scan(self, total_files, total_threats, threats):
        self.scanning = False
        self.progress_bar.stop()
        self.progress_bar.configure(mode="determinate")
        self.progress_bar.set(1.0)
        
        self.btn_scan.configure(state="normal")
        self.btn_browse.configure(state="normal")
        self.entry_path.configure(state="normal")
        self.progress_frame.grid_forget()

        if self.cancel_event.is_set():
            self.append_log("[WARN] Threat scan aborted by user request.\n", "warning")
            self.lbl_current_file.configure(text="Scan aborted.")
        else:
            self.append_log(f"\n[OK] Scan completed successfully.\n", "success")
            self.append_log(f"[INF] Total Hashed Files: {total_files}\n", "info")
            
            if total_threats > 0:
                self.append_log(f"[THREAT] Identified {total_threats} threats. Immediate cleanup recommended!\n", "threat")
                for file_p, threat_name, _ in threats:
                    self.append_log(f"  -> Threat Location: {file_p} ({threat_name})\n", "threat")
            else:
                self.append_log(f"[SUCCESS] Directory is completely secure. No threats detected.\n", "success")

    def cancel_scan(self):
        if self.scanning:
            self.cancel_event.set()
            self.append_log("[WARN] Aborting scan operations...\n", "warning")
