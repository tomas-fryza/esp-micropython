"""
SD card write and read example

MicroSD card adapter pins:
  MicroSD | ESP32
 ---------+----------
   VCC    | VCC (+5V)
   GND    | GND
   MISO   | GPIO19
   MOSI   | GPIO23
   SCK    | GPIO18
   CS     | GPIO12 (D13)

Author(s):
- M. Pugazhendi (muthuswamy.pugazhendi@gmail.com)
- Tomas Fryza

Creation date: 2025-06-05
Last modified: 2025-06-06

Inspired by:
  * https://www.instructables.com/ESP32-Micro-SD-Card-Interface/
  * https://www.engineersgarage.com/micropython-esp32-microsd-card/
"""

# MicroPython builtin modules
from machine import Pin, SPI
import os

# External modules
from sdcard import SDCard

# Setup SPI interface
spi = SPI(1,  # HSPI (or use 1 for VSPI)
          baudrate=1_320_000,
          sck=Pin(18),
          mosi=Pin(23),
          miso=Pin(19))

# Connect SD card
sd = SDCard(spi, Pin(12))

# Mount the SD card at /sd
os.mount(sd, '/sd')

# DPrint SD card directory and files
print("Files on SD card:")
print(os.listdir("/sd"))

# Create / Open a file in write mode
file = open("/sd/sample.txt", "w")
print("Writing to SD card...")

# Write sample text
for i in range(5):
    file.write(f"Hi there! " * (i+1))
    file.write("\r\n")
    
# Close the file
file.close()

# Again, open the file in "append mode" for appending a line
file = open("/sd/sample.txt", "a")
file.write("Appended sample text at the END\r\n")
file.close()

# Open the file in "read mode".
file = open("/sd/sample.txt", "r")
if file:
    print("Reading from SD card...")
    read_data = file.read()
    print(read_data)
file.close()
