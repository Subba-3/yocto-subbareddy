#!/bin/sh

echo "================================="
echo "   Subbu OS - WiFi Setup"
echo "================================="
echo ""

# Check wlan0 exists
if ! ip link show wlan0 > /dev/null 2>&1; then
    echo "ERROR: No WiFi adapter found (wlan0 missing)!"
    exit 1
fi

# Bring up wlan0
ip link set wlan0 up
sleep 1

# Scan networks
echo "Scanning for available networks..."
echo ""
NETWORKS=$(iw dev wlan0 scan 2>/dev/null | grep "SSID:" | \
    sed 's/.*SSID: //' | sed '/^$/d' | sort -u)

if [ -z "$NETWORKS" ]; then
    echo "No networks found. Try again."
    exit 1
fi

# Show numbered list
echo "Available Networks:"
echo "------------------"
i=1
echo "$NETWORKS" | while IFS= read -r ssid; do
    echo "$i. $ssid"
    i=$((i + 1))
done
echo ""

# Ask user to pick number
printf "Enter network number: "
read CHOICE

# Get selected SSID
SELECTED=$(echo "$NETWORKS" | sed -n "${CHOICE}p")

if [ -z "$SELECTED" ]; then
    echo "Invalid choice!"
    exit 1
fi

echo ""
echo "Selected: $SELECTED"
printf "Enter password: "
read -s PASSWORD
echo ""

# ── FIX: Create directory if it does not exist ──
mkdir -p /etc/wpa_supplicant
mkdir -p /run/wpa_supplicant

# Write wpa_supplicant config
echo "Configuring WiFi..."
cat > /etc/wpa_supplicant/wpa_supplicant.conf << WPAEOF
ctrl_interface=DIR=/run/wpa_supplicant
update_config=1
country=IN

network={
    ssid="$SELECTED"
    psk="$PASSWORD"
}
WPAEOF

# Kill old wpa_supplicant
killall wpa_supplicant 2>/dev/null
sleep 1

# Start wpa_supplicant
wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf
sleep 3

# Get IP via DHCP
echo "Getting IP address..."
udhcpc -i wlan0 -t 10 -q

sleep 3

# Check connection
IP=$(ip addr show wlan0 | grep "inet " | awk '{print $2}' | cut -d/ -f1)

if [ -n "$IP" ]; then
    echo ""
    echo "================================="
    echo "  WiFi Connected!"
    echo "  IP Address: $IP"
    echo "================================="
    echo ""
    # Enable SSH
    echo "Enabling SSH..."
    systemctl enable sshd 2>/dev/null || true
    systemctl start sshd 2>/dev/null || true
    echo "SSH Enabled!"
    echo "You can now SSH: ssh root@$IP"
else
    echo ""
    echo "================================="
    echo "  Connection Failed!"
    echo "  Check password and try again"
    echo "================================="
    exit 1
fi
