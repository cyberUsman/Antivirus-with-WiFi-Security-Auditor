import customtkinter as ctk
import sys
import os
import threading

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.cleaner_engine import scan_junk, clean_junk

class CleanerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.cleaning = False
        self.cancel_event = threading.Event()

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.header_label = ctk.CTkLabel(
            self, 
            text="Junk Cleaner", 
            font=ctk.CTkFont(size=26, weight="bold", family="Segoe UI"),
            text_color="#f8fafc"
        )
        self.header_label.grid(row=0, column=0, sticky="w", pady=(0, 20))

        self.setup_control_panel()

        self.setup_division_cards()

        self.progress_bar = ctk.CTkProgressBar(self, orientation="horizontal", progress_color="#0ea5e9")
        self.progress_bar.grid(row=2, column=0, sticky="ew", pady=(0, 15))
        self.progress_bar.grid_remove()

        self.setup_console()

        self.start_scan_junk()

    def setup_control_panel(self):
        self.control_panel = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.control_panel.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.control_panel.grid_columnconfigure(0, weight=1)

        self.lbl_junk_status = ctk.CTkLabel(
            self.control_panel, 
            text="Junk status: Calculating cache...", 
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"), 
            text_color="#0ea5e9"
        )
        self.lbl_junk_status.grid(row=0, column=0, padx=20, pady=(18, 5), sticky="w")

        self.lbl_junk_details = ctk.CTkLabel(
            self.control_panel, 
            text="Walking system TEMP directories to evaluate cache logs.", 
            font=ctk.CTkFont(size=12, family="Segoe UI"),
            text_color="#64748b"
        )
        self.lbl_junk_details.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="w")

        self.btn_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.btn_frame.grid(row=0, column=1, rowspan=2, padx=20, pady=15, sticky="e")

        self.btn_scan = ctk.CTkButton(
            self.btn_frame, 
            text="🔍 Scan Cache", 
            width=110,
            fg_color="#1e293b",
            text_color="#cbd5e1",
            hover_color="#334155",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            command=self.start_scan_junk
        )
        self.btn_scan.grid(row=0, column=0, padx=5)

        self.btn_clean = ctk.CTkButton(
            self.btn_frame, 
            text="🧹 Clean Now", 
            width=110, 
            fg_color="#10b981", 
            hover_color="#059669", 
            state="disabled",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            command=self.start_cleaning
        )
        self.btn_clean.grid(row=0, column=1, padx=5)

    def setup_division_cards(self):
        self.division_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.division_frame.grid_columnconfigure((0, 1), weight=1, uniform="equal")

        self.card_size = ctk.CTkFrame(self.division_frame, corner_radius=10, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.card_size.grid(row=0, column=0, padx=(0, 6), pady=0, sticky="nsew")
        self.lbl_size_title = ctk.CTkLabel(self.card_size, text="RECLAIMABLE CAPACITY", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_size_title.pack(padx=15, pady=(12, 2), anchor="w")
        self.lbl_size_val = ctk.CTkLabel(self.card_size, text="0 MB", font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI"), text_color="#0ea5e9")
        self.lbl_size_val.pack(padx=15, pady=(0, 12), anchor="w")

        self.card_files = ctk.CTkFrame(self.division_frame, corner_radius=10, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.card_files.grid(row=0, column=1, padx=(6, 0), pady=0, sticky="nsew")
        self.lbl_files_title = ctk.CTkLabel(self.card_files, text="FILES DETECTED", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_files_title.pack(padx=15, pady=(12, 2), anchor="w")
        self.lbl_files_val = ctk.CTkLabel(self.card_files, text="0 Files", font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI"), text_color="#cbd5e1")
        self.lbl_files_val.pack(padx=15, pady=(0, 12), anchor="w")

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
        self.txt_console.tag_config("item", foreground="#38bdf8")
        
        self.append_log("[INF] ShieldGuard Junk Cleaner initialized.\n", "info")

    def append_log(self, text, tag="info"):
        self.txt_console.configure(state="normal")
        self.txt_console.insert("end", text, tag)
        self.txt_console.see("end")
        self.txt_console.configure(state="disabled")

    def format_bytes(self, num_bytes):
        if num_bytes > 1024 * 1024 * 1024:
            return f"{num_bytes / 1024.0 / 1024.0 / 1024.0:.2f} GB"
        elif num_bytes > 1024 * 1024:
            return f"{num_bytes / 1024.0 / 1024.0:.1f} MB"
        elif num_bytes > 1024:
            return f"{num_bytes / 1024.0:.1f} KB"
        else:
            return f"{num_bytes} Bytes"

    def start_scan_junk(self):
        self.btn_scan.configure(state="disabled")
        self.btn_clean.configure(state="disabled")
        self.lbl_junk_status.configure(text="Scanning System Cache...", text_color="#0ea5e9")
        self.division_frame.grid_remove()
        
        def scan_thread():
            files, folders, size = scan_junk()
            self.after(0, lambda: self.finish_scan_junk(files, folders, size))

        t = threading.Thread(target=scan_thread)
        t.daemon = True
        t.start()

    def finish_scan_junk(self, files, folders, size):
        self.btn_scan.configure(state="normal")
        size_str = self.format_bytes(size)
        
        if size > 0:
            self.lbl_junk_status.configure(text="System Cache Junk Detected", text_color="#f59e0b")
            self.lbl_junk_details.configure(text="Select 'Clean Now' to delete temporary system logs and files safely.")
            
            self.lbl_size_val.configure(text=size_str)
            self.lbl_files_val.configure(text=f"{files} Files")
            self.division_frame.grid(row=2, column=0, sticky="ew", pady=(0, 15))
            
            self.btn_clean.configure(state="normal")
            self.append_log(f"[INF] Cache evaluated: {size_str} ({files} files) can be reclaimed.\n", "info")
        else:
            self.lbl_junk_status.configure(text="System Cache Clean", text_color="#10b981")
            self.lbl_junk_details.configure(text="No temporary log directories or cache files need removal.")
            self.btn_clean.configure(state="disabled")
            self.append_log("[OK] Scan complete. System temporary directory is clean.\n", "success")

    def start_cleaning(self):
        if self.cleaning:
            return
            
        self.cleaning = True
        self.cancel_event.clear()
        
        self.btn_scan.configure(state="disabled")
        self.btn_clean.configure(state="disabled")
        self.division_frame.grid_remove()
        
        self.progress_bar.grid()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        self.append_log("[INF] Executing directory purge on system TEMP path...\n", "info")

        def clean_thread():
            def progress(item_name, deleted_count, freed_bytes):
                freed_str = self.format_bytes(freed_bytes)
                self.lbl_junk_status.configure(text=f"Clearing: {deleted_count} files ({freed_str})", text_color="#0ea5e9")
                self.append_log(f"[PURGED] Reclaimed space -> {item_name}\n", "item")

            del_count, bytes_cleared = clean_junk(progress_callback=progress, cancel_event=self.cancel_event)
            self.after(0, lambda: self.finish_cleaning(del_count, bytes_cleared))

        t = threading.Thread(target=clean_thread)
        t.daemon = True
        t.start()

    def finish_cleaning(self, files_cleared, bytes_cleared):
        self.cleaning = False
        self.progress_bar.stop()
        self.progress_bar.grid_remove()
        
        self.btn_scan.configure(state="normal")
        
        size_freed = self.format_bytes(bytes_cleared)
        self.lbl_junk_status.configure(text="System Optimization Complete", text_color="#10b981")
        self.lbl_junk_details.configure(text=f"Successfully reclaimed {size_freed} of disk space.")
        
        self.append_log(f"\n[OK] Purge execution completed.\n", "success")
        self.append_log(f"[INF] Total Files Deleted: {files_cleared}\n", "info")
        self.append_log(f"[SUCCESS] Reclaimed Disk Space: {size_freed}\n", "success")
