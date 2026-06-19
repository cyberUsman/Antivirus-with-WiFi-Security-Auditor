import subprocess
import re
import sys
import json
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import db_manager


def scan_wifi_networks():
    networks = []
    is_mocked = False

    try:
        output = subprocess.check_output(
            ["netsh", "wlan", "show", "networks"],
            stderr=subprocess.STDOUT,
            creationflags=0x08000000
        )

        try:
            decoded_output = output.decode("utf-8")
        except UnicodeDecodeError:
            decoded_output = output.decode("cp1252", errors="ignore")

        networks = parse_netsh_output(decoded_output)

        if not networks:
            networks = get_mock_wifi_networks()
            is_mocked = True

    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        networks = get_mock_wifi_networks()
        is_mocked = True

    insecure_count = 0
    security_score = 100

    for net in networks:
        auth = net["auth"].upper()
        encryption = net["encryption"].upper()

        if "OPEN" in auth or "NONE" in encryption or "WEP" in auth:
            net["security_level"] = "Vulnerable (Open/WEP)"
            net["status"] = "Risk"
            insecure_count += 1
            security_score -= 20

        elif "WPA2" in auth or "WPA3" in auth:
            net["security_level"] = "Secure (WPA2/WPA3)"
            net["status"] = "Secure"

        else:
            net["security_level"] = "Weak (WPA/TKIP)"
            net["status"] = "Warning"
            security_score -= 10

    if security_score < 0:
        security_score = 0

    print(f"Security Score: {security_score}/100")

    details_str = json.dumps(networks)

    db_manager.log_wifi_audit(
        networks_found=len(networks),
        insecure_networks=insecure_count,
        details_str=details_str
    )

    return networks, insecure_count, is_mocked, security_score


def parse_netsh_output(text):
    networks = []

    blocks = re.split(r'SSID\s+\d+\s*:', text)

    for block in blocks[1:]:
        lines = block.splitlines()
        ssid = lines[0].strip() if lines else "Unknown SSID"

        if not ssid:
            ssid = "Hidden Network"

        auth = "Unknown"
        encryption = "Unknown"

        for line in lines:
            if "Authentication" in line:
                auth = line.split(":", 1)[1].strip()
            elif "Encryption" in line:
                encryption = line.split(":", 1)[1].strip()

        networks.append({
            "ssid": ssid,
            "auth": auth,
            "encryption": encryption
        })

    return networks


def get_mock_wifi_networks():
    return [
        {"ssid": "HomeSecure_5G", "auth": "WPA2-Personal", "encryption": "CCMP"},
        {"ssid": "CoffeeShop_Free_WiFi", "auth": "Open", "encryption": "None"},
        {"ssid": "Corporate_WPA3_Enterprise", "auth": "WPA3-Enterprise", "encryption": "CCMP"},
        {"ssid": "Airport_Public", "auth": "Open", "encryption": "None"},
        {"ssid": "Net_Vulnerable", "auth": "WEP", "encryption": "WEP"},
        {"ssid": "Neighborhood_Net", "auth": "WPA-Personal", "encryption": "TKIP"}
    ]