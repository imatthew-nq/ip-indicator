# IP Indicator for Ubuntu Desktop

A system tray indicator that displays your local and public IP addresses with a country flag emoji.

![Screenshot placeholder - The indicator shows your IPs in the system tray]

## Features

- 🌐 Shows public IP address with country flag in the system tray
- 💻 Displays local IP address in the menu
- 🔄 Auto-updates every 15 seconds
- ⚡ Lightweight and efficient

## Requirements

- Ubuntu 24.04 (or other Linux distributions with Ayatana AppIndicator support)
- Python 3
- GTK 3
- Ayatana AppIndicator 3

### Installation

1. Clone the repository:
```bash
git clone git@github.com:imatthew-nq/ip-indicator.git
cd ip-indicator
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

This will:
- Install required system dependencies
- Install the application to `/usr/local/bin/ip-indicator`
- (Optional) Enable autostart on login

### Manual Run

You can also run it directly without installing:
```bash
python3 ip_indicator.py
```

## Usage

Once running, you'll see an indicator in your system tray showing:
- A country flag emoji (🇺🇸, 🇬🇧, etc.)
- Your public IP address

Click on the indicator to see:
- 🌐 Your public IP address with country flag
- 💻 Your local IP address
- ❌ Quit option

The indicator updates automatically every 15 seconds.

## Troubleshooting

### Missing Dependencies Error

If you see:
```
ERROR: Missing required dependencies!
```

Make sure you have installed all system packages:
```bash
sudo apt install python3-gi gir1.2-ayatanaappindicator3-0.1 python3-requests
```

### Network Timeout

If your internet connection is slow, you might see timeout warnings in the terminal. The app will retry on the next update cycle (15 seconds).

### Indicator Not Showing

Make sure your desktop environment supports AppIndicators:
- **GNOME**: Install `gnome-shell-extension-appindicator`
  ```bash
  sudo apt install gnome-shell-extension-appindicator
  ```
- **Other DEs**: Usually work out of the box (XFCE, MATE, etc.)

## Privacy

This application:
- Makes requests to `api.ipify.org` to get your public IP
- Makes requests to `ip-api.com` to get country information
- Does not store or transmit any personal data

## License

Free to use and modify as needed.
