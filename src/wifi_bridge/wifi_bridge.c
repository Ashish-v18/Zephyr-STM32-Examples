#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/uart.h>
#include <string.h>
#include <stdlib.h>

#include "wifi_bridge.h"
#include "led_driver.h"

#define UART_DEVICE_NODE DT_NODELABEL(usart1)
static const struct device *uart_dev = DEVICE_DT_GET(UART_DEVICE_NODE);

#define RX_BUF_SIZE 64
static uint8_t rx_buf[RX_BUF_SIZE];
static int rx_buf_pos = 0;

// Message Queue to pass colors from ISR to Main Thread
struct led_msg {
    uint8_t r;
    uint8_t g;
    uint8_t b;
};

K_MSGQ_DEFINE(led_msgq, sizeof(struct led_msg), 10, 4);

// Command Parser: "C:255,0,0"
static void process_command(char *cmd)
{
    printk("[DEBUG] Processing command: '%s'\n", cmd);
    
    if (strncmp(cmd, "C:", 2) == 0) {
        int r, g, b;
        char *ptr = cmd + 2;
        
        r = strtol(ptr, &ptr, 10);
        if (*ptr == ',') ptr++;
        g = strtol(ptr, &ptr, 10);
        if (*ptr == ',') ptr++;
        b = strtol(ptr, NULL, 10);
        
        printk("[DEBUG] Parsed RGB: (%d, %d, %d)\n", r, g, b);
        
        // Send to message queue (safe from ISR)
        struct led_msg msg = { (uint8_t)r, (uint8_t)g, (uint8_t)b };
        k_msgq_put(&led_msgq, &msg, K_NO_WAIT);
        
    } else {
        printk("[DEBUG] Unknown command format\n");
    }
}

static void serial_cb(const struct device *dev, void *user_data)
{
    uint8_t c;

    if (!uart_irq_update(dev)) {
        return;
    }

    while (uart_irq_rx_ready(dev)) {
        uart_fifo_read(dev, &c, 1);
        
        // printk inside ISR can be risky if too frequent, but okay for debug
        // printk("[DEBUG] UART RX: 0x%02X ('%c')\n", c, (c >= 32 && c < 127) ? c : '.');

        if (c == '\n' || c == '\r') {
            rx_buf[rx_buf_pos] = '\0';
            if (rx_buf_pos > 0) {
                // Process command (now just pushes to queue)
                process_command((char *)rx_buf);
            }
            rx_buf_pos = 0;
        } else if (rx_buf_pos < (RX_BUF_SIZE - 1)) {
            rx_buf[rx_buf_pos++] = c;
        } else {
            rx_buf_pos = 0; // Overflow reset
        }
    }
}

void run_wifi_bridge(void)
{
    if (!device_is_ready(uart_dev)) {
        printk("UART device not ready\n");
        return;
    }

    // Initialize LED
    printk("Initializing LED driver...\n");
    if (led_ws2812_init() != 0) {
        printk("LED initialization failed!\n");
        return;
    }
    
    // Set LED to OFF initially
    printk("Setting LED to OFF...\n");
    led_ws2812_set_color(0, 0, 0);
    k_msleep(100);

    // Configure interrupt
    uart_irq_callback_user_data_set(uart_dev, serial_cb, NULL);
    uart_irq_rx_enable(uart_dev);
    
    printk("Wi-Fi Bridge Initialized. Listening on USART1 (D2/D8)...\n");
    
    struct led_msg msg;

    // Main Loop: Process messages from the queue
    while (1) {
        // Wait forever for a message
        if (k_msgq_get(&led_msgq, &msg, K_FOREVER) == 0) {
            printk("Wi-Fi Command: Set Color (%d, %d, %d)\n", msg.r, msg.g, msg.b);
            led_ws2812_set_color(msg.r, msg.g, msg.b);
            printk("[DEBUG] LED update complete\n");
        }
    }
}
