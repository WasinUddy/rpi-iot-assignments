#!/usr/bin/env python3
"""
Raspberry Pi LED Button Control
Press button to blink LED 3 times
"""

import RPi.GPIO as GPIO
import time

# GPIO Pin Configuration
BUTTON_PIN = 17  # GPIO pin for button
LED_PIN = 27     # GPIO pin for LED

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.output(LED_PIN, GPIO.LOW)

def blink_led(times=3, delay=0.5):
    """Blink LED specified number of times"""
    for _ in range(times):
        GPIO.output(LED_PIN, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(LED_PIN, GPIO.LOW)
        time.sleep(delay)

def button_callback(channel):
    """Callback function when button is pressed"""
    blink_led(3, 0.5)

# Setup button interrupt
GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=button_callback, bouncetime=200)

print("Button-LED Control System Started")
print("Press the button to blink LED 3 times")
print("Press Ctrl+C to exit")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down...")
finally:
    GPIO.cleanup()
    print("GPIO cleaned up")

