#include <zephyr/kernel.h>
#include <zephyr/device.h>
#include <zephyr/drivers/spi.h>
#include <zephyr/sys/printk.h>
#include <string.h>

#include "led_driver.h"

#define SPI_FREQ 4000000U
#define BYTES_PER_LED 24 // 3 colors * 8 bits * 1 byte/bit = 24 bytes
#define RESET_BYTES 50   // 50 bytes * 2μs = 100μs
#define BUFFER_SIZE (BYTES_PER_LED + RESET_BYTES)
#define SPI1_NODE DT_NODELABEL(spi1)

static const struct device *spi;
static struct spi_config cfg;
static uint8_t buf[BUFFER_SIZE];
static struct spi_buf tx = {.buf = buf, .len = sizeof(buf)};
static struct spi_buf_set txs = {.buffers = &tx, .count = 1};

/* --- Encoding helpers --- */
static void encode_byte(uint8_t c, uint8_t *out, int *idx)
{
    for (int b = 7; b >= 0; --b)
    {
        uint8_t bit = (c >> b) & 1;
        // '0': 0x40, '1': 0x70
        out[(*idx)++] = bit ? 0x70 : 0x40;
    }
}

static void set_pixel_internal(uint8_t *buf, int *idx, uint8_t r, uint8_t g, uint8_t b)
{
    // LED Color Order: GRB (Standard WS2812B)
    encode_byte(g, buf, idx);
    encode_byte(r, buf, idx);
    encode_byte(b, buf, idx);
}

int led_ws2812_init(void)
{
    printk("Initializing WS2812 LED...\n");
    spi = DEVICE_DT_GET(SPI1_NODE);
    if (!device_is_ready(spi))
    {
        printk("SPI1 NOT READY!\n");
        return -1;
    }

    cfg.frequency = SPI_FREQ;
    cfg.operation = SPI_WORD_SET(8) | SPI_TRANSFER_MSB;
    cfg.slave = 0;

    return 0;
}

void led_ws2812_set_color(uint8_t r, uint8_t g, uint8_t b)
{
    int idx = 0;
    memset(buf, 0, sizeof(buf));
    set_pixel_internal(buf, &idx, r, g, b);
    spi_write(spi, &cfg, &txs);
}

void run_rgb(void)
{
    // Legacy function - just runs a demo loop
    if (led_ws2812_init() != 0)
        return;

    while (1)
    {
        printk("Setting Red\n");
        led_ws2812_set_color(255, 0, 0);
        k_msleep(1000);

        printk("Setting Green\n");
        led_ws2812_set_color(0, 255, 0);
        k_msleep(1000);

        printk("Setting Blue\n");
        led_ws2812_set_color(0, 0, 255);
        k_msleep(1000);

        printk("Setting Off\n");
        led_ws2812_set_color(0, 0, 0);
        k_msleep(1000);
    }
}
