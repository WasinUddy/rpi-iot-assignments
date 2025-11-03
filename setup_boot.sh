#!/bin/bash
# One-line boot setup script for LED Button Control
# Usage: sudo bash setup_boot.sh

set -e

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_PATH="$REPO_ROOT/assignments-1/led_button.py"
SERVICE_FILE="/etc/systemd/system/led-button.service"

echo "Setting up LED Button Control to run on boot..."

# Create systemd service file
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=LED Button Control
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=$REPO_ROOT/assignments-1
ExecStart=/usr/bin/python3 $SCRIPT_PATH
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Reload systemd and enable service
sudo systemctl daemon-reload
sudo systemctl enable led-button.service
sudo systemctl start led-button.service

echo "✓ Setup complete!"
echo "✓ Service enabled and started"
echo ""
echo "Check status with: sudo systemctl status led-button.service"
echo "View logs with: sudo journalctl -u led-button.service -f"

