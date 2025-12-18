cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(rtos_project)

# Add component directories to include path
target_include_directories(app PRIVATE 
    src
    src/led_driver 
    src/wifi_bridge
)

# List sources
target_sources(app PRIVATE
    src/main.c
    src/led_driver/led_driver.c
    src/wifi_bridge/wifi_bridge.c
    
    # Examples
    src/examples/ex_blinky.c
    src/examples/ex_math.c
    # src/examples/ex_sem.c
)
