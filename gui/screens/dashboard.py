import customtkinter as ctk
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from database import db_manager

class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller

        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.setup_header()

        self.setup_status_banner()

        self.setup_stat_cards()

        self.setup_activity_log()

        self.refresh_dashboard()

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))

        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="System Overview", 
            font=ctk.CTkFont(size=26, weight="bold", family="Segoe UI"),
            text_color="#f8fafc"
        )
        self.title_label.pack(side="left")

        self.btn_refresh = ctk.CTkButton(
            self.header_frame,
            text="🔄 Refresh System Stats",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            width=160,
            height=34,
            fg_color="#1e293b",
            text_color="#94a3b8",
            hover_color="#334155",
            command=self.refresh_dashboard
        )
        self.btn_refresh.pack(side="right")

    def setup_status_banner(self):
        self.banner_frame = ctk.CTkFrame(self, corner_radius=12, height=70, border_width=1)
        self.banner_frame.grid(row=1, column=0, sticky="ew", pady=(0, 20))
        self.banner_frame.pack_propagate(False)

        self.banner_lbl = ctk.CTkLabel(
            self.banner_frame,
            text="Checking System Security Status...",
            font=ctk.CTkFont(size=16, weight="bold", family="Segoe UI"),
            anchor="w"
        )
        self.banner_lbl.pack(side="left", padx=20, fill="both", expand=True)

    def setup_stat_cards(self):
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.grid(row=2, column=0, sticky="ew", pady=(0, 20))
        self.cards_frame.grid_columnconfigure((0, 1, 2, 3), weight=1, uniform="equal")

        self.card_status = ctk.CTkFrame(self.cards_frame, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.card_status.grid(row=0, column=0, padx=6, pady=5, sticky="nsew")
        self.lbl_status_title = ctk.CTkLabel(self.card_status, text="SYSTEM STATUS", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_status_title.pack(padx=15, pady=(15, 2), anchor="w")
        self.lbl_status_val = ctk.CTkLabel(self.card_status, text="Checking...", font=ctk.CTkFont(size=20, weight="bold", family="Segoe UI"))
        self.lbl_status_val.pack(padx=15, pady=(0, 5), anchor="w")
        self.lbl_status_sub = ctk.CTkLabel(self.card_status, text="Live defense monitoring", font=ctk.CTkFont(size=10, family="Segoe UI"), text_color="#475569")
        self.lbl_status_sub.pack(padx=15, pady=(0, 15), anchor="w")

        self.card_threats = ctk.CTkFrame(self.cards_frame, corner_radius=12, border_width=1, border_color="#f43f5e", fg_color="#111827")
        self.card_threats.grid(row=0, column=1, padx=6, pady=5, sticky="nsew")
        self.lbl_threats_title = ctk.CTkLabel(self.card_threats, text="THREATS BLOCKED", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_threats_title.pack(padx=15, pady=(15, 2), anchor="w")
        self.lbl_threats_val = ctk.CTkLabel(self.card_threats, text="0", font=ctk.CTkFont(size=22, weight="bold", family="Segoe UI"), text_color="#f43f5e")
        self.lbl_threats_val.pack(padx=15, pady=(0, 5), anchor="w")
        self.lbl_threats_sub = ctk.CTkLabel(self.card_threats, text="Signatures detected", font=ctk.CTkFont(size=10, family="Segoe UI"), text_color="#475569")
        self.lbl_threats_sub.pack(padx=15, pady=(0, 15), anchor="w")

        self.card_junk = ctk.CTkFrame(self.cards_frame, corner_radius=12, border_width=1, border_color="#0ea5e9", fg_color="#111827")
        self.card_junk.grid(row=0, column=2, padx=6, pady=5, sticky="nsew")
        self.lbl_junk_title = ctk.CTkLabel(self.card_junk, text="DISK SPACE FREED", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_junk_title.pack(padx=15, pady=(15, 2), anchor="w")
        self.lbl_junk_val = ctk.CTkLabel(self.card_junk, text="0 MB", font=ctk.CTkFont(size=22, weight="bold", family="Segoe UI"), text_color="#0ea5e9")
        self.lbl_junk_val.pack(padx=15, pady=(0, 5), anchor="w")
        self.lbl_junk_sub = ctk.CTkLabel(self.card_junk, text="Temporary files cleared", font=ctk.CTkFont(size=10, family="Segoe UI"), text_color="#475569")
        self.lbl_junk_sub.pack(padx=15, pady=(0, 15), anchor="w")

        self.card_wifi = ctk.CTkFrame(self.cards_frame, corner_radius=12, border_width=1, border_color="#f59e0b", fg_color="#111827")
        self.card_wifi.grid(row=0, column=3, padx=6, pady=5, sticky="nsew")
        self.lbl_wifi_title = ctk.CTkLabel(self.card_wifi, text="WIFI SECURITY", font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"), text_color="#64748b")
        self.lbl_wifi_title.pack(padx=15, pady=(15, 2), anchor="w")
        self.lbl_wifi_val = ctk.CTkLabel(self.card_wifi, text="0 Audited", font=ctk.CTkFont(size=22, weight="bold", family="Segoe UI"), text_color="#f59e0b")
        self.lbl_wifi_val.pack(padx=15, pady=(0, 5), anchor="w")
        self.lbl_wifi_sub = ctk.CTkLabel(self.card_wifi, text="Network strength & cipher", font=ctk.CTkFont(size=10, family="Segoe UI"), text_color="#475569")
        self.lbl_wifi_sub.pack(padx=15, pady=(0, 15), anchor="w")

    def setup_activity_log(self):
        self.activity_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.activity_frame.grid(row=3, column=0, sticky="nsew", pady=(0, 5))
        self.activity_frame.grid_rowconfigure(1, weight=1)
        self.activity_frame.grid_columnconfigure(0, weight=1)

        self.activity_header = ctk.CTkFrame(self.activity_frame, fg_color="transparent")
        self.activity_header.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        
        self.lbl_log_title = ctk.CTkLabel(
            self.activity_header, 
            text="📋 Recent Security Timeline", 
            font=ctk.CTkFont(size=15, weight="bold", family="Segoe UI"),
            text_color="#f8fafc"
        )
        self.lbl_log_title.pack(side="left")

        self.scroll_feed = ctk.CTkScrollableFrame(self.activity_frame, fg_color="transparent")
        self.scroll_feed.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 15))

    def refresh_dashboard(self):
        stats = db_manager.get_dashboard_stats()
        activities = db_manager.get_recent_activities()

        if stats["total_threats"] > 0:
            self.banner_frame.configure(fg_color="#450a0a", border_color="#f43f5e")
            self.banner_lbl.configure(
                text="⚠️ ALERT: Malware threats detected on your system. Run a full scan to clean.", 
                text_color="#fecdd3"
            )
            self.lbl_status_val.configure(text="Threats Found", text_color="#f43f5e")
            self.card_status.configure(border_color="#f43f5e")
        elif stats["last_wifi_insecure"] > 0:
            self.banner_frame.configure(fg_color="#451a03", border_color="#f59e0b")
            self.banner_lbl.configure(
                text=f"⚠️ WARNING: Audited Wi-Fi has {stats['last_wifi_insecure']} insecure or open connections.",
                text_color="#fef3c7"
            )
            self.lbl_status_val.configure(text="WiFi Vulnerable", text_color="#f59e0b")
            self.card_status.configure(border_color="#f59e0b")
        else:
            self.banner_frame.configure(fg_color="#064e3b", border_color="#10b981")
            self.banner_lbl.configure(
                text="🟢 System Secured: No active malware or insecure beacons detected.", 
                text_color="#d1fae5"
            )
            self.lbl_status_val.configure(text="Protected", text_color="#10b981")
            self.card_status.configure(border_color="#10b981")

        self.lbl_threats_val.configure(text=f"{stats['total_threats']}")
        
        freed = stats["total_bytes_freed"]
        if freed > 1024 * 1024 * 1024:
            junk_txt = f"{freed / 1024.0 / 1024.0 / 1024.0:.2f} GB"
        elif freed > 1024 * 1024:
            junk_txt = f"{freed / 1024.0 / 1024.0:.1f} MB"
        elif freed > 1024:
            junk_txt = f"{freed / 1024.0:.1f} KB"
        else:
            junk_txt = f"{freed} B"
        self.lbl_junk_val.configure(text=junk_txt)

        wifi_val_txt = f"{stats['last_wifi_total']} Beacons"
        if stats["last_wifi_insecure"] > 0:
            wifi_val_txt += f" ({stats['last_wifi_insecure']} Risk)"
            self.lbl_wifi_val.configure(text=wifi_val_txt, text_color="#f59e0b")
        else:
            self.lbl_wifi_val.configure(text=wifi_val_txt, text_color="#10b981")

        for child in self.scroll_feed.winfo_children():
            child.destroy()

        if not activities:
            no_action_lbl = ctk.CTkLabel(
                self.scroll_feed, 
                text="No recent actions found. Select a task in the sidebar.", 
                font=ctk.CTkFont(size=12, slant="italic", family="Segoe UI"),
                text_color="#475569"
            )
            no_action_lbl.pack(pady=40)
            return

        for index, act in enumerate(activities):
            item_frame = ctk.CTkFrame(self.scroll_feed, fg_color="#0f172a", corner_radius=8, border_width=1, border_color="#1e293b")
            item_frame.pack(fill="x", pady=5, padx=5)

            theme_color = "#0ea5e9"
            icon = "⚡"
            if "Cleaner" in act["type"]:
                theme_color = "#0ea5e9"
                icon = "🧹"
            elif "WiFi" in act["type"]:
                theme_color = "#f59e0b"
                icon = "📶"
            elif "Antivirus" in act["type"]:
                theme_color = "#f43f5e"
                icon = "🛡️"

            badge_frame = ctk.CTkFrame(item_frame, fg_color=theme_color, corner_radius=6, width=110, height=28)
            badge_frame.pack(side="left", padx=12, pady=10)
            badge_frame.pack_propagate(False)

            badge_lbl = ctk.CTkLabel(
                badge_frame, 
                text=f"{icon} {act['type']}", 
                font=ctk.CTkFont(size=10, weight="bold", family="Segoe UI"),
                text_color="#ffffff" if theme_color != "#f59e0b" else "#000000"
            )
            badge_lbl.pack(expand=True)

            msg_lbl = ctk.CTkLabel(
                item_frame, 
                text=act["msg"], 
                font=ctk.CTkFont(size=12, family="Segoe UI"),
                text_color="#cbd5e1",
                anchor="w"
            )
            msg_lbl.pack(side="left", fill="x", expand=True, padx=10)

            time_lbl = ctk.CTkLabel(
                item_frame, 
                text=act["timestamp"], 
                font=ctk.CTkFont(size=11, family="Segoe UI"),
                text_color="#64748b"
            )
            time_lbl.pack(side="right", padx=15)
