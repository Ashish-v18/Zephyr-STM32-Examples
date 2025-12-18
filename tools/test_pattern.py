#!/usr/bin/env python3
"""
Interactive LED Pattern Tester
Cycles through various colors and patterns to test the Wi-Fi LED control system.
"""

import socket
import time
import sys

# Pico IP Address
PICO_IP = "192.168.0.106"
PORT = 8080

def send_color(r, g, b, label=""):
    """Send a color command to the Pico."""
    cmd = f"C:{r},{g},{b}\n"
    
    if label:
        print(f"[{label}] ", end="")
    print(f"RGB({r:3d}, {g:3d}, {b:3d}) -> ", end="", flush=True)
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((PICO_IP, PORT))
        s.send(cmd.encode())
        
        response = s.recv(1024)
        print(f"✓ {response.decode().strip()}")
        
        s.close()
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_primary_colors():
    """Test primary RGB colors."""
    print("\n=== Testing Primary Colors ===")
    colors = [
        (255, 0, 0, "Red"),
        (0, 255, 0, "Green"),
        (0, 0, 255, "Blue"),
    ]
    
    for r, g, b, name in colors:
        send_color(r, g, b, name)
        time.sleep(1)

def test_secondary_colors():
    """Test secondary colors."""
    print("\n=== Testing Secondary Colors ===")
    colors = [
        (255, 255, 0, "Yellow"),
        (255, 0, 255, "Magenta"),
        (0, 255, 255, "Cyan"),
    ]
    
    for r, g, b, name in colors:
        send_color(r, g, b, name)
        time.sleep(1)

def test_white_levels():
    """Test different white brightness levels."""
    print("\n=== Testing White Brightness Levels ===")
    levels = [255, 192, 128, 64, 32, 0]
    
    for level in levels:
        send_color(level, level, level, f"{int(level/255*100)}%")
        time.sleep(0.8)

def test_rainbow_cycle():
    """Cycle through rainbow colors."""
    print("\n=== Rainbow Cycle ===")
    
    # Red -> Yellow -> Green -> Cyan -> Blue -> Magenta -> Red
    steps = 20
    for i in range(steps * 6):
        phase = i / steps
        
        if phase < 1:  # Red to Yellow
            r, g, b = 255, int(255 * phase), 0
        elif phase < 2:  # Yellow to Green
            r, g, b = int(255 * (2 - phase)), 255, 0
        elif phase < 3:  # Green to Cyan
            r, g, b = 0, 255, int(255 * (phase - 2))
        elif phase < 4:  # Cyan to Blue
            r, g, b = 0, int(255 * (4 - phase)), 255
        elif phase < 5:  # Blue to Magenta
            r, g, b = int(255 * (phase - 4)), 0, 255
        else:  # Magenta to Red
            r, g, b = 255, 0, int(255 * (6 - phase))
        
        send_color(r, g, b, f"Step {i+1}/{steps*6}")
        time.sleep(0.1)

def test_breathing():
    """Breathing effect (fade in/out)."""
    print("\n=== Breathing Effect (Red) ===")
    
    for cycle in range(2):
        # Fade in
        for i in range(0, 256, 8):
            send_color(i, 0, 0, f"Fade In {i}")
            time.sleep(0.05)
        
        # Fade out
        for i in range(255, -1, -8):
            send_color(i, 0, 0, f"Fade Out {i}")
            time.sleep(0.05)

def test_strobe():
    """Strobe effect."""
    print("\n=== Strobe Effect ===")
    
    for i in range(10):
        send_color(255, 255, 255, "ON")
        time.sleep(0.1)
        send_color(0, 0, 0, "OFF")
        time.sleep(0.1)

def interactive_mode():
    """Interactive color picker."""
    print("\n=== Interactive Mode ===")
    print("Enter RGB values (0-255) or 'q' to quit")
    
    while True:
        try:
            user_input = input("\nEnter R G B (e.g., '255 0 0'): ").strip()
            
            if user_input.lower() in ['q', 'quit', 'exit']:
                break
            
            parts = user_input.split()
            if len(parts) != 3:
                print("Error: Please enter 3 values (R G B)")
                continue
            
            r, g, b = map(int, parts)
            
            if not all(0 <= v <= 255 for v in [r, g, b]):
                print("Error: Values must be between 0 and 255")
                continue
            
            send_color(r, g, b, "Custom")
            
        except ValueError:
            print("Error: Please enter valid numbers")
        except KeyboardInterrupt:
            print("\nExiting...")
            break

def main():
    """Main menu."""
    print("=" * 60)
    print("Wi-Fi LED Pattern Tester")
    print(f"Target: {PICO_IP}:{PORT}")
    print("=" * 60)
    
    # Test connection first
    print("\nTesting connection...")
    if not send_color(0, 0, 0, "Connection Test"):
        print("\n❌ Cannot connect to Pico. Please check:")
        print("  1. Pico is powered and connected to Wi-Fi")
        print("  2. IP address is correct")
        print("  3. You're on the same network")
        sys.exit(1)
    
    print("\n✓ Connection successful!")
    
    menu = """
Select a test pattern:
  1. Primary Colors (R, G, B)
  2. Secondary Colors (Y, M, C)
  3. White Brightness Levels
  4. Rainbow Cycle
  5. Breathing Effect
  6. Strobe Effect
  7. Interactive Mode
  8. Run All Tests
  0. Turn Off LED and Exit

Choice: """
    
    while True:
        try:
            choice = input(menu).strip()
            
            if choice == '1':
                test_primary_colors()
            elif choice == '2':
                test_secondary_colors()
            elif choice == '3':
                test_white_levels()
            elif choice == '4':
                test_rainbow_cycle()
            elif choice == '5':
                test_breathing()
            elif choice == '6':
                test_strobe()
            elif choice == '7':
                interactive_mode()
            elif choice == '8':
                test_primary_colors()
                test_secondary_colors()
                test_white_levels()
                test_rainbow_cycle()
            elif choice == '0':
                print("\nTurning off LED...")
                send_color(0, 0, 0, "OFF")
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                
        except KeyboardInterrupt:
            print("\n\nTurning off LED...")
            send_color(0, 0, 0, "OFF")
            print("Goodbye!")
            break

if __name__ == "__main__":
    main()
