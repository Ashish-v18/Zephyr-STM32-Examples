#!/bin/bash

# Simple LED test sequence with visual feedback

echo "🌈 LED Color Test Sequence"
echo "=========================="
echo ""
echo "Watch your LED! It should change colors..."
echo ""

echo "🔴 Testing RED..."
python3 tools/test_wifi_led.py 255 0 0
sleep 2

echo "🟢 Testing GREEN..."
python3 tools/test_wifi_led.py 0 255 0
sleep 2

echo "🔵 Testing BLUE..."
python3 tools/test_wifi_led.py 0 0 255
sleep 2

echo "🟡 Testing YELLOW..."
python3 tools/test_wifi_led.py 255 255 0
sleep 2

echo "🟣 Testing MAGENTA..."
python3 tools/test_wifi_led.py 255 0 255
sleep 2

echo "🔵 Testing CYAN..."
python3 tools/test_wifi_led.py 0 255 255
sleep 2

echo "⚪ Testing WHITE..."
python3 tools/test_wifi_led.py 255 255 255
sleep 2

echo "⚫ Turning OFF..."
python3 tools/test_wifi_led.py 0 0 0

echo ""
echo "✅ Test sequence complete!"
echo ""
echo "Did the LED change colors?"
echo "If NOT, check:"
echo "  1. LED has 5V power (Nucleo 5V → LED VCC)"
echo "  2. LED data wire (Nucleo PA7 → LED DIN)"
echo "  3. Common ground (GND → GND)"
