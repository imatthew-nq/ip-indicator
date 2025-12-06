#!/usr/bin/env python3
import sys
import socket
import requests

try:
    import gi
    gi.require_version("Gtk", "3.0")
    gi.require_version("AyatanaAppIndicator3", "0.1")
    from gi.repository import Gtk, GLib, AyatanaAppIndicator3 as AppIndicator
except (ImportError, ValueError) as e:
    print("ERROR: Missing required dependencies!", file=sys.stderr)
    print("Please install required packages:", file=sys.stderr)
    print("  sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1 python3-requests", file=sys.stderr)
    print(f"\nDetails: {e}", file=sys.stderr)
    sys.exit(1)

APP_ID = "ip-indicator"
REQUEST_TIMEOUT = 5  # seconds

def get_local_ip():
    """Get local IP address using multiple methods for better reliability."""
    try:
        # Method 1: Connect to external host (doesn't actually send data)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        s.connect(('8.8.8.8', 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        pass
    
    try:
        # Method 2: Use hostname resolution
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        if local_ip and local_ip != "127.0.0.1":
            return local_ip
    except:
        pass
    
    return "N/A"

def get_ips_and_flag():
    """Fetch local IP, public IP, and country flag."""
    local_ip = get_local_ip()

    public_ip, flag = "N/A", "🌐"
    try:
        # Get public IP with timeout
        response = requests.get("https://api.ipify.org", timeout=REQUEST_TIMEOUT)
        public_ip = response.text.strip()
        
        # Get country information
        info = requests.get(f"http://ip-api.com/json/{public_ip}", timeout=REQUEST_TIMEOUT).json()
        country_code = info.get("countryCode", "")
        if country_code:
            flag = country_code_to_emoji(country_code)
    except requests.exceptions.Timeout:
        print("WARNING: Network request timed out", file=sys.stderr)
    except requests.exceptions.RequestException as e:
        print(f"WARNING: Could not fetch public IP: {e}", file=sys.stderr)
    except Exception as e:
        print(f"WARNING: Unexpected error: {e}", file=sys.stderr)

    return local_ip, public_ip, flag

def country_code_to_emoji(country_code):
    # Convert 2-letter country code (e.g. "DE") into emoji flag 🇩🇪
    return ''.join([chr(0x1F1E6 + ord(c) - ord('A')) for c in country_code.upper()])

def build_menu():
    menu = Gtk.Menu()
    local_ip, public_ip, flag = get_ips_and_flag()

    item_public = Gtk.MenuItem(label=f"{flag} Public: {public_ip}")
    item_local = Gtk.MenuItem(label=f"💻 Local: {local_ip}")
    quit_item = Gtk.MenuItem(label="❌ Quit")

    quit_item.connect("activate", quit)
    menu.append(item_public)
    menu.append(item_local)
    menu.append(quit_item)

    menu.show_all()
    return menu

def update_indicator(ind):
    _, public_ip, flag = get_ips_and_flag()
    ind.set_label(f"{flag} {public_ip}", "")
    return True

def main():
    ind = AppIndicator.Indicator.new(APP_ID, "network-wired", AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    ind.set_status(AppIndicator.IndicatorStatus.ACTIVE)

    ind.set_menu(build_menu())
    update_indicator(ind)

    GLib.timeout_add_seconds(15, update_indicator, ind)  # update every 15s
    Gtk.main()

if __name__ == "__main__":
    main()

