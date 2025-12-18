#!/bin/bash
# Simple script to check Nucleo output

echo "Checking Nucleo serial ports..."
echo ""
echo "Press Ctrl+C after a few seconds"
echo ""

# Try first port
echo "=== Checking /dev/tty.usbmodem11203 ==="
timeout 3 cat /dev/tty.usbmodem11203 2>/dev/null && echo "" || echo "No output or error"

echo ""
echo "=== Checking /dev/tty.usbmodem11301 ==="
timeout 3 cat /dev/tty.usbmodem11301 2>/dev/null && echo "" || echo "No output or error"

echo ""
echo "Done."
