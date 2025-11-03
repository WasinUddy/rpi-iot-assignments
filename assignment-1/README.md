# LED Button Control - Assignment 1

A simple Raspberry Pi project that blinks an LED 3 times when a button is pressed.

## Hardware Requirements
- Raspberry Pi (4, 3B+, Zero, etc.)
- Push Button
- LED (5mm or 3mm)
- 220Ω Resistor (for LED)
- 10kΩ Resistor (optional, for button debouncing)
- Jumper wires
- Breadboard (optional)

## Wiring Diagram

```
Raspberry Pi GPIO Pin Layout (BCM):

Button Setup:
  - Button Pin 1 → GPIO 17 (BCM)
  - Button Pin 2 → Ground (GND)

LED Setup:
  - LED Anode (long leg) → GPIO 27 (BCM) via 220Ω Resistor
  - LED Cathode (short leg) → Ground (GND)

Physical Pins on Raspberry Pi:
  ┌─────────────────────────┐
  │ GPIO 17 (Button) → Pin 11
  │ GPIO 27 (LED)    → Pin 13
  │ GND              → Pin 6 or 9 or 14 or 20 or 25 or 30 or 34 or 39
  └─────────────────────────┘
```

### Simplified Connection Guide
1. **Button**: Connect one pin to GPIO 17, other pin to GND
2. **LED**: Connect anode (long leg) to GPIO 27 through 220Ω resistor, cathode (short leg) to GND

## Installation & Setup

### 1. Install Required Libraries
```bash
sudo apt-get update
sudo apt-get install python3-rpi.gpio python3-pip
```

### 2. Run the Script Manually
```bash
cd /path/to/assignments-1
sudo python3 led_button.py
```

### 3. Set Up to Run on Boot
Run this command from the repository root to set up automatic startup:
```bash
sudo bash -c 'echo "[Unit]\nDescription=LED Button Control\nAfter=network.target\n\n[Service]\nType=simple\nUser=pi\nWorkingDirectory=$(pwd)/assignments-1\nExecStart=/usr/bin/python3 $(pwd)/assignments-1/led_button.py\nRestart=on-failure\nRestartSec=10\n\n[Install]\nWantedBy=multi-user.target" > /etc/systemd/system/led-button.service && sudo systemctl daemon-reload && sudo systemctl enable led-button.service && sudo systemctl start led-button.service'
```

Or manually (step-by-step):
```bash
# Create service file
sudo nano /etc/systemd/system/led-button.service

# Paste the content from led-button.service file

# Enable and start
sudo systemctl daemon-reload
sudo systemctl enable led-button.service
sudo systemctl start led-button.service
```

### 4. Check Service Status
```bash
sudo systemctl status led-button.service
```

### 5. View Logs
```bash
sudo journalctl -u led-button.service -f
```

## Usage

1. **Manual Run**: Execute `sudo python3 led_button.py`
2. **Press Button**: The LED will blink 3 times
3. **Stop**: Press Ctrl+C to exit
4. **Boot Run**: After setup, the script runs automatically on system boot

## GPIO Configuration

- **Button Pin**: GPIO 17 (BCM numbering)
- **LED Pin**: GPIO 27 (BCM numbering)
- **Blink Count**: 3 times
- **Blink Delay**: 0.5 seconds per blink
- **Button Debounce**: 200ms

## Troubleshooting

1. **"No module named RPi.GPIO"**: Install with `sudo apt-get install python3-rpi.gpio`
2. **"Permission denied"**: Run with `sudo`
3. **LED not blinking**: Check connections and GPIO pin numbers
4. **Service not starting**: Check logs with `sudo journalctl -u led-button.service`
5. **Script keeps restarting**: Check for errors in logs

## Files

- `led_button.py` - Main Python script
- `led-button.service` - Systemd service file (for boot setup)
- `README.md` - This file

