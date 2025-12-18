import network
import socket
import time
import select
from machine import UART, Pin

# --- Configuration ---
SSID = "USHA"
PASSWORD = "usharesidency"
HTTP_PORT = 80
TCP_PORT = 8080
UART_ID = 0
UART_TX = 0  # GP0
UART_RX = 1  # GP1
BAUDRATE = 115200

# --- HTML loader (serves index.html from filesystem) ---
def load_html(filename="index.html"):
    try:
        with open(filename, "r") as f:
            return f.read()
    except OSError:
        return "<!DOCTYPE html><html><body><h1>index.html not found</h1></body></html>"

# --- Init UART ---
uart = UART(UART_ID, baudrate=BAUDRATE, tx=Pin(UART_TX), rx=Pin(UART_RX))
print(f"UART initialized on GP{UART_TX}/GP{UART_RX} at {BAUDRATE} baud")

# --- Connect to Wi-Fi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print(f"Connecting to {SSID}...")
max_wait = 20
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('waiting for connection...')
    time.sleep(1)

if wlan.status() != 3:
    raise RuntimeError(f"Network connection failed. Status={wlan.status()}")

print("Connected")
ip_address = wlan.ifconfig()[0]
print(f"IP Address: {ip_address}")
print(f"OPEN THIS IN YOUR BROWSER: http://{ip_address}")

# --- Setup Sockets ---
# HTTP Server (Port 80)
http_sock = socket.socket()
http_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
http_sock.bind(('0.0.0.0', HTTP_PORT))
http_sock.listen(5)

# Raw TCP Server (Port 8080) - For backward compatibility
tcp_sock = socket.socket()
tcp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp_sock.bind(('0.0.0.0', TCP_PORT))
tcp_sock.listen(5)

print(f"HTTP Server listening on port {HTTP_PORT}")
print(f"TCP Server listening on port {TCP_PORT}")

# --- Main Loop ---
while True:
    try:
        # Check for activity on both sockets
        r, _, _ = select.select([http_sock, tcp_sock], [], [])

        for s in r:
            if s is http_sock:
                # Handle Web Browser Request
                cl, addr = http_sock.accept()
                request = cl.recv(1024).decode()

                # Debug: show every HTTP request
                print("----- HTTP REQUEST FROM", addr, "-----")
                print(request)

                first_line = request.split("\r\n", 1)[0]
                # Example first_line: "GET /set?r=255&g=0&b=0 HTTP/1.1"
                if first_line.startswith("GET /set?"):
                    try:
                        # Extract query string between ? and space
                        qs = first_line.split("?", 1)[1].split(" ", 1)[0]
                        pairs = qs.split("&")
                        r_val, g_val, b_val = 0, 0, 0
                        for p in pairs:
                            if "=" in p:
                                key, val = p.split("=", 1)
                                if key == "r":
                                    r_val = int(val)
                                elif key == "g":
                                    g_val = int(val)
                                elif key == "b":
                                    b_val = int(val)

                        cmd = "C:{},{},{}\n".format(r_val, g_val, b_val)
                        uart.write(cmd)
                        print("Web Command:", cmd.strip())

                        cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\n\r\nOK')
                    except Exception as e:
                        print("Parse error:", e)
                        cl.send('HTTP/1.0 400 Bad Request\r\n\r\nError')
                else:
                    # Serve HTML file
                    html = load_html()
                    cl.send('HTTP/1.0 200 OK\r\nContent-Type: text/html\r\n\r\n')
                    cl.send(html)

                cl.close()

            elif s is tcp_sock:
                # Handle Raw TCP Request (Legacy)
                cl, addr = tcp_sock.accept()
                print(f"TCP Client connected from {addr}")
                data = cl.recv(1024)
                if data:
                    print(f"TCP Received: {data}")
                    uart.write(data)
                    cl.send(b"OK\n")
                cl.close()

    except Exception as e:
        print("Error in main loop:", e)
