#!/bin/sh

# This should be done by /etc/rc.local or something on boot.

echo 17 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio17/direction
chmod 766 /sys/class/gpio/gpio17/value

echo 27 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio27/direction
chmod 766 /sys/class/gpio/gpio27/value

echo 22 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio22/direction
chmod 766 /sys/class/gpio/gpio22/value

echo 23 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio23/direction
chmod 766 /sys/class/gpio/gpio23/value

echo 24 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio24/direction
chmod 766 /sys/class/gpio/gpio24/value

echo 25 > /sys/class/gpio/export
echo out > /sys/class/gpio/gpio25/direction
chmod 766 /sys/class/gpio/gpio25/value
