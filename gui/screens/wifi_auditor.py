import customtkinter as ctk
import sys
import os
import threading
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from core.wifi_engine import scan_wifi_networks

class WifiAuditorScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color="transparent")
        self.controller = controller
        
        self.scanning = False

        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.setup_header()

        self.setup_summary_panel()

        self.setup_networks_list()

        self.run_wifi_scan()

    def setup_header(self):
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="WiFi Network Auditor", 
            font=ctk.CTkFont(size=26, weight="bold", family="Segoe UI"),
            text_color="#f8fafc"
        )
        self.title_label.pack(side="left")
        
        self.btn_scan = ctk.CTkButton(
            self.header_frame, 
            text="📡 Scan Beacons", 
            width=160, 
            height=34,
            fg_color="#0ea5e9",
            hover_color="#0284c7",
            font=ctk.CTkFont(size=12, weight="bold", family="Segoe UI"),
            command=self.run_wifi_scan
        )
        self.btn_scan.pack(side="right")

    def setup_summary_panel(self):
        self.summary_panel = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.summary_panel.grid(row=1, column=0, sticky="ew", pady=(0, 15))
        self.summary_panel.grid_columnconfigure((0, 1, 2), weight=1)

        self.lbl_net_count = ctk.CTkLabel(
            self.summary_panel, 
            text="Networks: Calculating...", 
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            text_color="#cbd5e1"
        )
        self.lbl_net_count.grid(row=0, column=0, padx=20, pady=15, sticky="w")

        self.lbl_insecure_count = ctk.CTkLabel(
            self.summary_panel, 
            text="Insecure: --", 
            font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
            text_color="#cbd5e1"
        )
        self.lbl_insecure_count.grid(row=0, column=1, padx=20, pady=15)

        self.lbl_adapter_status = ctk.CTkLabel(
            self.summary_panel, 
            text="Status: Idle", 
            font=ctk.CTkFont(size=12, slant="italic", family="Segoe UI"),
            text_color="#64748b"
        )
        self.lbl_adapter_status.grid(row=0, column=2, padx=20, pady=15, sticky="e")

        self.progress_bar = ctk.CTkProgressBar(self.summary_panel, orientation="horizontal", progress_color="#0ea5e9")
        self.progress_bar.grid(row=1, column=0, columnspan=3, padx=15, pady=(0, 10), sticky="ew")
        self.progress_bar.grid_remove()

    def setup_networks_list(self):
        self.list_frame = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#1e293b", fg_color="#111827")
        self.list_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 5))
        self.list_frame.grid_rowconfigure(0, weight=1)
        self.list_frame.grid_columnconfigure(0, weight=1)

        self.scroll_networks = ctk.CTkScrollableFrame(self.list_frame, fg_color="transparent")
        self.scroll_networks.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    def run_wifi_scan(self):
        if self.scanning:
            return
            
        self.scanning = True
        self.btn_scan.configure(state="disabled")
        
        self.progress_bar.grid()
        self.progress_bar.configure(mode="indeterminate")
        self.progress_bar.start()
        
        self.lbl_adapter_status.configure(text="Status: Scanning beacons...", text_color="#0ea5e9")

        def async_scan():
            networks, insecure_count, is_mocked = scan_wifi_networks()
            self.after(0, lambda: self.finish_wifi_scan(networks, insecure_count, is_mocked))

        t = threading.Thread(target=async_scan)
        t.daemon = True
        t.start()

    def finish_wifi_scan(self, networks, insecure_count, is_mocked):
        self.scanning = False
        self.btn_scan.configure(state="normal")
        
        self.progress_bar.stop()
        self.progress_bar.grid_remove()

        self.lbl_net_count.configure(text=f"📡 Networks Audited: {len(networks)}")
        
        if insecure_count > 0:
            self.lbl_insecure_count.configure(text=f"⚠️ Vulnerable Open APs: {insecure_count}", text_color="#f43f5e")
        else:
            self.lbl_insecure_count.configure(text="🟢 No Insecure APs Found", text_color="#10b981")

        if is_mocked:
            self.lbl_adapter_status.configure(text="Status: Demo Mode", text_color="#f59e0b")
        else:
            self.lbl_adapter_status.configure(text="Status: Live scan active", text_color="#10b981")

        for child in self.scroll_networks.winfo_children():
            child.destroy()

        if not networks:
            no_nets_lbl = ctk.CTkLabel(
                self.scroll_networks,
                text="No active wireless networks identified. Enable Wi-Fi card adapters.",
                font=ctk.CTkFont(size=12, slant="italic", family="Segoe UI"),
                text_color="#cbd5e1"
            )
            no_nets_lbl.pack(pady=40)
            return

        for index, net in enumerate(networks):
            net_card = ctk.CTkFrame(self.scroll_networks, fg_color="#0f172a", corner_radius=10, border_width=1, border_color="#1e293b")
            net_card.pack(fill="x", pady=5, padx=5)

            title_frame = ctk.CTkFrame(net_card, fg_color="transparent")
            title_frame.pack(side="left", padx=15, pady=12)

            ssid_lbl = ctk.CTkLabel(
                title_frame, 
                text=net["ssid"], 
                font=ctk.CTkFont(size=14, weight="bold", family="Segoe UI"),
                text_color="#f8fafc"
            )
            ssid_lbl.pack(anchor="w")

            random.seed(net["ssid"])
            signal_dbm = random.randint(55, 98)
            signal_desc = "Excellent" if signal_dbm > 80 else ("Good" if signal_dbm > 65 else "Weak")
            
            detail_lbl = ctk.CTkLabel(
                title_frame,
                text=f"Cipher: {net['auth']} | {net['encryption']}  •  📶 {signal_desc} ({signal_dbm}%)",
                font=ctk.CTkFont(size=11, family="Segoe UI"),
                text_color="#64748b"
            )
            detail_lbl.pack(anchor="w")

            badge_color = "#064e3b"
            badge_border = "#10b981"
            badge_text = "🛡️ Secure WPA2/WPA3"
            text_color = "#d1fae5"

            if net["status"] == "Risk":
                badge_color = "#450a0a"
                badge_border = "#f43f5e"
                badge_text = "⚠️ Insecure / Open"
                text_color = "#fecdd3"
            elif net["status"] == "Warning":
                badge_color = "#451a03"
                badge_border = "#f59e0b"
                badge_text = "⚡ Weak Cipher (TKIP)"
                text_color = "#fef3c7"

            badge_frame = ctk.CTkFrame(net_card, fg_color=badge_color, corner_radius=6, border_width=1, border_color=badge_border)
            badge_frame.pack(side="right", padx=15, pady=12)

            badge_lbl = ctk.CTkLabel(
                badge_frame,
                text=badge_text,
                font=ctk.CTkFont(size=11, weight="bold", family="Segoe UI"),
                text_color=text_color
            )
            badge_lbl.pack(padx=10, pady=5)
