#ifndef WIFI_BRIDGE_H
#define WIFI_BRIDGE_H

/**
 * @brief Initialize and run the UART-based Wi-Fi bridge.
 * 
 * This function initializes the UART interrupt and LED driver,
 * then enters an infinite loop waiting for commands from the message queue.
 */
void run_wifi_bridge(void);

#endif /* WIFI_BRIDGE_H */
