#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include "ex_math.h"

void run_math(void)
{
    int a = 10;
    int b = 20;
    int c = a + b;
    printk("Math Example: %d + %d = %d\n", a, b, c);
}
