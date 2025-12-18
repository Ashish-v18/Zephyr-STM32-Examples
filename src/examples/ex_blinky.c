#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/sys/printk.h>
#include "ex_blinky.h"

#define LED0_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED0_NODE, gpios);

void run_blinky(void)
{
    if (!gpio_is_ready_dt(&led))
    {
        return;
    }

    int ret = gpio_pin_configure_dt(&led, GPIO_OUTPUT_ACTIVE);
    if (ret < 0)
    {
        return;
    }

    while (1)
    {
        gpio_pin_toggle_dt(&led);
        k_msleep(1000);
        printk("LED Toggled\n");
    }
}
