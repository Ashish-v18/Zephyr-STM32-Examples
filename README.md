# 🛜 Wi-Fi Controlled LED System

A hybrid IoT system using **Raspberry Pi Pico 2W** as a Wi-Fi modem and **STM32 Nucleo-G070RB** running Zephyr RTOS as a real-time LED controller.

---

## 🔌 Hardware Setup

### **1. Wiring Connections (CRITICAL)**

| Pico 2W Pin | Nucleo Pin | Function |
| :--- | :--- | :--- |
| **GP0** (TX) | **D2** (PA10) | UART Data (Pico → Nucleo) |
| **GP1** (RX) | **D8** (PA9) | UART Data (Nucleo → Pico) |
| **GND** | **GND** | Common Ground |

> **Note:** We use Nucleo pins **D2/D8 (USART1)** instead of D0/D1 to avoid conflict with the USB debugger.

### **2. LED Connection**

| Nucleo Pin | WS2812 LED | Function |
| :--- | :--- | :--- |
| **PA7** (MOSI) | **DIN** | Data Input |
| **5V** | **VCC** | Power |
| **GND** | **GND** | Ground |

---

## � Zephyr Development Setup

### **1. Activate Environment**
Before running any Zephyr commands, you must activate the virtual environment:
```bash
source ~/Developer/zephyrproject/.venv/bin/activate
```

### **2. Build Firmware**
Build the project for the STM32 Nucleo-G070RB board:
```bash
cd ~/Developer/RTOS_Project
west build -b nucleo_g070rb -p always
```

### **3. Flash Firmware**
Connect the Nucleo board via USB and flash the firmware:
```bash
west flash -r openocd
```

### **4. Monitor Serial Output**
To view debug logs from the Nucleo (e.g., "Wi-Fi Bridge Initialized"):
```bash
ls -la /dev/tty.usbmodem*    
picocom -b 115200 /dev/tty.usbmodem11203
```
*(Replace `11203` with your actual Nucleo USB port)*

---

## 🐍 Pico Development Setup (MicroPython)

### **1. Upload Firmware**
To upload the `main.py` script to the Pico 2W:
```bash
# Install mpremote if needed
pip3 install mpremote

# Upload file
mpremote connect /dev/tty.usbmodem11301 cp pico_script/main.py :main.py
```

### **2. Reset Pico**
```bash
mpremote connect /dev/tty.usbmodem11301 reset
```

---

## 🚀 Usage Guide

### **Control the LED**
Run the Python test script from your computer to send commands over Wi-Fi:

```bash
# Syntax: python3 tools/test_wifi_led.py <Red> <Green> <Blue>

# Red
python3 tools/test_wifi_led.py 255 0 0

# Green
python3 tools/test_wifi_led.py 0 255 0

# Blue
python3 tools/test_wifi_led.py 0 0 255

# Off
python3 tools/test_wifi_led.py 0 0 0
```

### **Run Demo Sequence**
Cycle through all colors automatically:
```bash
./tools/test_led_sequence.sh
```
