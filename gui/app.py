import customtkinter as ctk
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.screens.dashboard import DashboardScreen
from gui.screens.file_scanner import FileScannerScreen
from gui.screens.cleaner import CleanerScreen
from gui.screens.wifi_auditor import WifiAuditorScreen

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("ShieldGuard - Desktop Security & WiFi Auditor")
        self.geometry("1080x700")
        self.minsize(980, 600)

        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#0b0f19")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.current_screen = None
        self.screen_classes = {
            "dashboard": DashboardScreen,
            "scanner": FileScannerScreen,
            "cleaner": CleanerScreen,
            "wifi": WifiAuditorScreen
        }

        self.setup_sidebar()
        self.setup_container()
        self.select_frame_by_name("dashboard")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#0f172a", border_width=1, border_color="#1e293b")
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(6, weight=1)

        self.logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.logo_frame.grid(row=0, column=0, padx=20, pady=(35, 45), sticky="ew")

        self.logo_icon = ctk.CTkLabel(
            self.logo_frame,
            text="🛡️",
            font=ctk.CTkFont(size=28)
        )
        self.logo_icon.pack(side="left", padx=(0, 2))

        self.logo_title_frame = ctk.CTkFrame(self.logo_frame, fg_color="transparent")
        self.logo_title_frame.pack(side="left")

        self.logo_label = ctk.CTkLabel(
            self.logo_title_frame, 
            text="ShieldGuard", 
            font=ctk.CTkFont(size=18, weight="bold", family="Segoe UI"),
            text_color="#0ea5e9"
        )
        self.logo_label.pack(anchor="w")

        self.logo_sub = ctk.CTkLabel(
            self.logo_title_frame,
            text="CORE SECURITY",
            font=ctk.CTkFont(size=9, weight="bold", family="Segoe UI"),
            text_color="#64748b"
        )
        self.logo_sub.pack(anchor="w")

        self.btn_dashboard = ctk.CTkButton(
            self.sidebar_frame, 
            text="   Dashboard", 
            anchor="w",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            fg_color="transparent",
            text_color="#94a3b8",
            hover_color="#1e293b",
            command=lambda: self.select_frame_by_name("dashboard")
        )
        self.btn_dashboard.grid(row=1, column=0, padx=15, pady=6, sticky="ew")

        self.btn_scanner = ctk.CTkButton(
            self.sidebar_frame, 
            text="   Antivirus Scanner", 
            anchor="w",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            fg_color="transparent",
            text_color="#94a3b8",
            hover_color="#1e293b",
            command=lambda: self.select_frame_by_name("scanner")
        )
        self.btn_scanner.grid(row=2, column=0, padx=15, pady=6, sticky="ew")

        self.btn_cleaner = ctk.CTkButton(
            self.sidebar_frame, 
            text="   Junk Cleaner", 
            anchor="w",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            fg_color="transparent",
            text_color="#94a3b8",
            hover_color="#1e293b",
            command=lambda: self.select_frame_by_name("cleaner")
        )
        self.btn_cleaner.grid(row=3, column=0, padx=15, pady=6, sticky="ew")

        self.btn_wifi = ctk.CTkButton(
            self.sidebar_frame, 
            text="   WiFi Auditor", 
            anchor="w",
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(size=13, weight="bold", family="Segoe UI"),
            fg_color="transparent",
            text_color="#94a3b8",
            hover_color="#1e293b",
            command=lambda: self.select_frame_by_name("wifi")
        )
        self.btn_wifi.grid(row=4, column=0, padx=15, pady=6, sticky="ew")

        self.footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.footer_frame.grid(row=7, column=0, padx=20, pady=25, sticky="ew")

        self.status_dot = ctk.CTkLabel(
            self.footer_frame,
            text="●",
            text_color="#10b981",
            font=ctk.CTkFont(size=12)
        )
        self.status_dot.pack(side="left", padx=(0, 6))

        self.version_label = ctk.CTkLabel(
            self.footer_frame, 
            text="System Protected", 
            font=ctk.CTkFont(size=11, weight="bold", family="Segoe UI"),
            text_color="#475569"
        )
        self.version_label.pack(side="left")

        self.nav_buttons = {
            "dashboard": self.btn_dashboard,
            "scanner": self.btn_scanner,
            "cleaner": self.btn_cleaner,
            "wifi": self.btn_wifi
        }

    def setup_container(self):
        self.container_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.container_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.container_frame.grid_rowconfigure(0, weight=1)
        self.container_frame.grid_columnconfigure(0, weight=1)

    def select_frame_by_name(self, name):
        for btn_name, btn in self.nav_buttons.items():
            if btn_name == name:
                btn.configure(fg_color="#0ea5e9", text_color="#ffffff", hover_color="#0284c7")
            else:
                btn.configure(fg_color="transparent", text_color="#94a3b8", hover_color="#1e293b")

        if self.current_screen is not None:
            self.current_screen.destroy()

        screen_class = self.screen_classes[name]
        self.current_screen = screen_class(self.container_frame, self)
        self.current_screen.grid(row=0, column=0, sticky="nsew")

if __name__ == "__main__":
    app = App()
    app.mainloop()
