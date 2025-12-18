// ex_sem.c
//#include <zephyr/kernel.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/sys/printk.h>
#include "ex_sem.h"


// ----- LED -----
#define LED_NODE DT_ALIAS(led0)
static const struct gpio_dt_spec led = GPIO_DT_SPEC_GET(LED_NODE, gpios);

// ----- Semaphore -----
static struct k_sem sem; // binary semaphore (0 or 1)

// ----- Threads -----
#define SEM_STACK 1024
#define SEM_PRIO 5

void producer_thread(void *, void *, void *);
void consumer_thread(void *, void *, void *);

K_THREAD_DEFINE(prod_id, SEM_STACK, producer_thread,
                NULL, NULL, NULL,
                SEM_PRIO, 0, 0);

K_THREAD_DEFINE(cons_id, SEM_STACK, consumer_thread,
                NULL, NULL, NULL,
                SEM_PRIO + 1, 0, 0);

// ----- Producer: gives semaphore every 1 second -----
void producer_thread(void *p1, void *p2, void *p3)
{
    while (1)
    {
        printk("Producer: giving semaphore\n");
        k_sem_give(&sem);
        k_msleep(1000);
    }
}

// ----- Consumer: waits for semaphore -----
void consumer_thread(void *p1, void *p2, void *p3)
{
    int ret;

    if (!gpio_is_ready_dt(&led))
    {
        printk("LED init failed\n");
        return;
    }
    gpio_pin_configure_dt(&led, GPIO_OUTPUT_INACTIVE);

    while (1)
    {
        printk("Consumer: waiting...\n");

        ret = k_sem_take(&sem, K_FOREVER); // block here

        if (ret == 0)
        {
            printk("Consumer: semaphore received! Toggling LED\n");
            gpio_pin_toggle_dt(&led);
        }
    }
}

void ex_sem_start(void)
{
    k_sem_init(&sem, 0, 1); // binary semaphore, initial = 0
    printk("Semaphore example started\n");
}
