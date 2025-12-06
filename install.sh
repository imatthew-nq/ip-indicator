#!/bin/bash

# IP Indicator Installation Script for Ubuntu 24.04
set -e

echo "IP Indicator Installation"
echo "========================="
echo ""

# Check if running on Ubuntu/Debian-based system
if ! command -v apt &> /dev/null; then
    echo "ERROR: This script is designed for Ubuntu/Debian-based systems."
    exit 1
fi

# Install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y python3-gi gir1.2-ayatanaappindicator3-0.1 python3-requests

echo ""
echo "✓ Dependencies installed successfully!"
echo ""

# Install application to /usr/local/bin
echo "Installing application..."
sudo cp ip_indicator.py /usr/local/bin/ip-indicator
sudo chmod +x /usr/local/bin/ip-indicator
echo "✓ Application installed to /usr/local/bin/ip-indicator"
echo ""

# Ask about autostart
read -p "Do you want to enable autostart? (y/n) " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Get the absolute path to the script
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    # Generate local desktop file pointing to installed command
    echo "Generating desktop file..."
    cat > "${SCRIPT_DIR}/ip-indicator.desktop" << EOF
[Desktop Entry]
Type=Application
Name=IP Indicator
Comment=System tray indicator showing local and public IP addresses
Exec=ip-indicator
Icon=network-workgroup
Terminal=false
Categories=Network;Utility;
StartupNotify=false
EOF
    
    # Create autostart directory
    mkdir -p ~/.config/autostart
    
    # Create desktop file pointing to installed command
    cat > ~/.config/autostart/ip-indicator.desktop << EOF
[Desktop Entry]
Type=Application
Name=IP Indicator
Comment=System tray indicator showing local and public IP addresses
Exec=ip-indicator
Icon=network-workgroup
Terminal=false
Categories=Network;Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
    
    echo "✓ Autostart enabled!"
    echo ""
fi

# Check if GNOME and suggest extension
if [ "$XDG_CURRENT_DESKTOP" = "GNOME" ] || [ "$XDG_CURRENT_DESKTOP" = "ubuntu:GNOME" ]; then
    echo "GNOME detected. For the indicator to show in the system tray, you need:"
    echo "  sudo apt install gnome-shell-extension-appindicator"
    echo ""
    read -p "Install GNOME AppIndicator extension now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt install -y gnome-shell-extension-appindicator
        echo "✓ Extension installed! You may need to log out and back in."
        echo ""
    fi
fi

echo "Installation complete!"
echo ""
echo "To start the IP Indicator, run:"
echo "  ip-indicator"
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Or enable autostart manually."
    echo ""
fi
