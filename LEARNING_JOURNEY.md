# 🎓 Project Learning Journey

This document maps the theoretical concepts we learned to their practical implementation in this repository.

---

## 1. Real-Time Operating System (Zephyr RTOS)

### **Interrupt Service Routines (ISR)**
*   **Concept:** A function that executes immediately when a hardware event occurs, interrupting the main CPU flow.
*   **Implementation:** `src/wifi_cmd.c`
    *   **Function:** `serial_cb()`
    *   **What it does:** Triggers whenever a byte is received over UART. It reads the byte and stores it in a buffer.
    *   **Key Lesson:** ISRs must be fast! We initially crashed the system (Kernel Panic) by trying to control the LED (which uses `sleep`) directly inside the ISR.

### **Inter-Thread Communication (Message Queues)**
*   **Concept:** Safely passing data between an Interrupt (ISR) and a Thread without race conditions.
*   **Implementation:** `src/wifi_cmd.c`
    *   **Object:** `K_MSGQ_DEFINE(led_msgq, ...)`
    *   **Usage:** The ISR (`serial_cb`) pushes parsed color data into the queue. The main loop (`run_wifi_bridge`) waits for data (`k_msgq_get`) and processes it.
    *   **Why:** This decoupled the time-critical ISR from the slower LED update logic.

### **Device Tree (DTS)**
*   **Concept:** A hardware description language used to configure pins and peripherals without hardcoding addresses.
*   **Implementation:** `nucleo_g070rb.overlay`
    *   **Usage:** We enabled `usart1` on pins `PA9` (D8) and `PA10` (D2) to avoid conflict with the default USB console.
    *   **Snippet:** `pinctrl-0 = <&usart1_tx_pa9 &usart1_rx_pa10>;`

---

## 2. Embedded Protocols

### **UART (Universal Asynchronous Receiver-Transmitter)**
*   **Concept:** Serial communication between two independent devices.
*   **Implementation:**
    *   **Nucleo Side:** `src/wifi_cmd.c` (Receives commands like "C:255,0,0").
    *   **Pico Side:** `pico_script/main.py` (Forwards Wi-Fi data to UART).
    *   **Key Lesson:** We learned about **Bus Contention** when the Pico tried to talk on D0/D1, which was already being driven by the ST-Link USB debugger.

### **SPI (Serial Peripheral Interface)**
*   **Concept:** High-speed synchronous serial protocol.
*   **Implementation:** `src/ex_rgb_ws2812.c`
    *   **Usage:** Used to drive the WS2812 LED. The LED requires precise timing (800kHz), which we achieved using the SPI peripheral instead of bit-banging.

---

## 3. IoT & Networking (MicroPython)

### **Socket Programming**
*   **Concept:** Creating network endpoints for communication.
*   **Implementation:** `pico_script/main_web.py`
    *   **TCP Server:** Listens on port 8080 for raw text commands.
    *   **HTTP Server:** Listens on port 80 to serve a web page.

### **Non-Blocking I/O (Select)**
*   **Concept:** Handling multiple network connections (HTTP and TCP) simultaneously without freezing.
*   **Implementation:** `pico_script/main_web.py`
    *   **Function:** `select.select([http_sock, tcp_sock], ...)`
    *   **Why:** Allows the Pico to serve a web page to your phone *and* listen for Python script commands at the same time.

---

## 4. Hardware Debugging

### **Bus Contention**
*   **Problem:** Pico connected to D0/D1 (USART2) resulted in no data received.
*   **Cause:** The on-board ST-Link debugger was also driving those pins.
*   **Solution:** Moved wires to D2/D8 (USART1) and updated the Device Tree.

### **Color Encoding (Endianness/Format)**
*   **Problem:** Sending "Green" turned the LED "Red".
*   **Cause:** The WS2812 LED hardware expected **GRB** (Green-Red-Blue) order, but we were sending **RGB**.
*   **Solution:** Fixed in `src/ex_rgb_ws2812.c` by reordering the bytes before sending via SPI.
