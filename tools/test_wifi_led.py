import socket
import time
import sys

# Pico IP Address (from your output)
PICO_IP = "192.168.0.109"
PORT = 8080

def send_color(r, g, b):
    cmd = f"C:{r},{g},{b}\n"
    print(f"Sending: {cmd.strip()} to {PICO_IP}:{PORT}")
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((PICO_IP, PORT))
        s.send(cmd.encode())
        
        # Optional: Wait for response if your Pico sends one (it sends "OK\n")
        response = s.recv(1024)
        print(f"Response: {response.decode().strip()}")
        
        s.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        r, g, b = sys.argv[1], sys.argv[2], sys.argv[3]
    else:
        print("Usage: python3 test_wifi_led.py <R> <G> <B>")
        print("Defaulting to Red (255, 0, 0)")
        r, g, b = 255, 0, 0
        
    send_color(r, g, b)
