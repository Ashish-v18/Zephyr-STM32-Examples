#!/usr/bin/env python3
"""
Debug script to monitor Nucleo's serial output
This will help identify if the Nucleo is receiving UART data
"""

import serial
import sys
import time

# Try both possible Nucleo ports
POSSIBLE_PORTS = ['/dev/tty.usbmodem11203', '/dev/tty.usbmodem11301']
BAUD_RATE = 115200

def find_nucleo_port():
    """Try to identify which port is the Nucleo"""
    print("Searching for Nucleo...")
    for port in POSSIBLE_PORTS:
        try:
            ser = serial.Serial(port, BAUD_RATE, timeout=1)
            print(f"\n✓ Found device on {port}")
            print("Monitoring for 5 seconds...")
            print("-" * 60)
            
            start_time = time.time()
            while time.time() - start_time < 5:
                if ser.in_waiting > 0:
                    data = ser.readline()
                    try:
                        print(f"[{port}] {data.decode('utf-8', errors='ignore').strip()}")
                    except:
                        print(f"[{port}] {data}")
            
            ser.close()
            print("-" * 60)
            print()
            
        except Exception as e:
            print(f"✗ Could not open {port}: {e}")
    
    print("\nDone checking ports.")

if __name__ == "__main__":
    print("=" * 60)
    print("Nucleo UART Monitor")
    print("=" * 60)
    print("\nThis script will check both USB serial ports")
    print("and display any output from the Nucleo.\n")
    
    find_nucleo_port()
    
    print("\nIf you saw 'Wi-Fi Bridge Initialized' message,")
    print("the Nucleo is running correctly.")
    print("\nIf no output, the Nucleo firmware may not be flashed.")
