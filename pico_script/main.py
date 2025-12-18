import network
import socket
import time
import select
from machine import UART, Pin

# --- Configuration ---
SSID = "USHA"
PASSWORD = "usharesidency"

HTTP_PORT = 80      # Browser UI
TCP_PORT = 8080     # Terminal / raw control

UART_ID = 0
UART_TX = 0  # GP0
UART_RX = 1  # GP1
BAUDRATE = 115200

# --- Load HTML from file ---
def load_html(filename="index.html"):
    try:
        with open(filename, "r") as f:
            return f.read()
    except:
        return "<html><body><h1>index.html not found</h1></body></html>"

# --- Init UART ---
uart = UART(UART_ID, baudrate=BAUDRATE, tx=Pin(UART_TX), rx=Pin(UART_RX))
print(f"UART initialized on GP{UART_TX}/GP{UART_RX} at {BAUDRATE} baud")

# --- Blink LED ---
led = Pin("LED", Pin.OUT)
for _ in range(4):
    led.toggle()
    time.sleep(0.2)

print("Booting...")

# --- WiFi ---
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to WiFi...")
for _ in range(20):
    if wlan.isconnected():
        break
    time.sleep(1)

if not wlan.isconnected():
    raise RuntimeError("WiFi connection failed!")

ip = wlan.ifconfig()[0]
print("Connected, IP:", ip)

# --- HTTP server ---
http = socket.socket()
http.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
http.bind(('0.0.0.0', HTTP_PORT))
http.listen(5)

# --- TCP server ---
tcp = socket.socket()
tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcp.bind(('0.0.0.0', TCP_PORT))
tcp.listen(5)

print("HTTP Server:", HTTP_PORT)
print("TCP  Server:", TCP_PORT)

# --- Main Loop ---
while True:
    try:
        readable, _, _ = select.select([http, tcp], [], [])

        for sock in readable:

            # -------- Browser --------
            if sock is http:
                cl, addr = http.accept()
                req = cl.recv(1024).decode()
                print("\n[HTTP]\n", req)

                first = req.split("\r\n")[0]

                if first.startswith("GET /set?"):
                    try:
                        qs = first.split("?",1)[1].split(" ",1)[0]
                        values = dict(x.split("=") for x in qs.split("&"))

                        r = int(values.get("r", 0))
                        g = int(values.get("g", 0))
                        b = int(values.get("b", 0))

                        cmd = f"C:{r},{g},{b}\n"
                        uart.write(cmd)

                        print("WEB → UART:", cmd.strip())

                        cl.send("HTTP/1.1 200 OK\r\n\r\nOK")
                    except Exception as e:
                        print("Parse error:", e)
                        cl.send("HTTP/1.1 400 Bad\r\n\r\nERROR")

                else:
                    html = load_html()
                    cl.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n")
                    cl.send(html)

                cl.close()

            # -------- Terminal --------
            elif sock is tcp:
                cl, addr = tcp.accept()
                print("TCP Client:", addr)

                try:
                    while True:
                        data = cl.recv(1024)
                        if not data:
                            break

                        print("TCP → UART:", data)
                        uart.write(data)
                        cl.send(b"OK\n")

                except:
                    pass
                finally:
                    cl.close()
                    print("TCP Client closed")

    except Exception as e:
        print("Loop error:", e)
