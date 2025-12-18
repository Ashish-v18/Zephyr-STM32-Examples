#ifndef LED_DRIVER_H
#define LED_DRIVER_H

#include <stdint.h>

/**
 * @brief Initialize the WS2812 LED driver.
 * 
 * @return int 0 on success, negative errno code on failure.
 */
int led_ws2812_init(void);

/**
 * @brief Set the color of the WS2812 LED.
 * 
 * @param r Red component (0-255)
 * @param g Green component (0-255)
 * @param b Blue component (0-255)
 */
void led_ws2812_set_color(uint8_t r, uint8_t g, uint8_t b);

/**
 * @brief Run a demo RGB loop.
 */
void run_rgb(void);

#endif /* LED_DRIVER_H */
