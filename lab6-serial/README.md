# Lab 6: I2C serial communication

* [Pre-Lab preparation](#preparation)
* [Part 1: I2C bus](#part1)
* [Part 2: I2C scanner](#part2)
* [Part 3: Communication with I2C devices](#part3)
* [Part 4: OLED display 128x64](#part4)
* [Challenges](#challenges)
* [References](#references)

### Component list
 
* ESP32 board with pre-installed MicroPython firmware, USB cable
* Breadboard
* RTC DS3231 and AT24C32 EEPROM memory module
  * Optional: DHT12 humidity/temperature sensor
  * Optional: GY-521 module with MPU-6050 microelectromechanical systems
* SH1106 I2C OLED display 128x64
* Logic analyzer
* Jumper wires

  ![photo_oled](images/photo_oled2.jpg)

### Learning objectives

* Understand the I2C communication
* Perform data transfers between ESP32 and I2C devices
* Use methods for OLED dispaly in MicroPython
* Use logic analyzer

<a name="preparation"></a>

## Pre-Lab preparation

1. Use pinout of the FireBeetle ESP32 board and find out on which pins the SDA and SCL signals are located.

2. Remind yourself, what the general structure of [I2C address and data frame](https://www.electronicshub.org/basics-i2c-communication/) is.

<a name="part1"></a>

## Part 1: I2C bus

I2C (Inter-Integrated Circuit) is a serial communication protocol designed for a two-wire interface, enabling the connection of low-speed devices such as sensors, EEPROMs, A/D and D/A converters, I/O interfaces, and other similar peripherals within embedded systems. Originally developed by Philips, this protocol has gained widespread adoption and is now utilized by nearly all major IC manufacturers.

I2C utilizes just two wires: **SCL** (Serial Clock) and **SDA** (Serial Data). Both of these wires should be connected to a resistor and pulled up to +Vdd. Additionally, I2C level shifters are available for connecting two I2C buses with different voltage levels.

In an I2C bus configuration, there is always one **Master** device and one or more **Slave** devices. Each Slave device is identified by a [unique address](https://i2c.info/).

![I2C bus](images/i2c-bus.png)

The initial I2C specifications defined maximum clock frequency of 100 kHz. This was later increased to 400 kHz as Fast mode. There is also a High speed mode which can go up to 3.4 MHz and there is also a 5 MHz ultra-fast mode.

In idle state both lines (SCL and SDA) are high. The communication is initiated by the master device. It generates the Start condition (S) followed by the address of the slave device (SLA). If the bit 0 of the address byte was set to 0 the master device will write to the slave device (SLA+W). Otherwise, the next byte will be read from the slave device (SLA+R). Each byte is supplemented by an ACK (low level) or NACK (high level) acknowledgment bit, which is always transmitted by the device receiving the previous byte.

The address byte is followed by one or more data bytes, where each contains 8 bits and is again terminated by ACK/NACK. Once all bytes are read or written the master device generates Stop condition (P). This means that the master device switches the SDA line from low voltage level to high voltage level before the SCL line switches from [high to low](https://www.electronicshub.org/basics-i2c-communication/).

![I2C protocol](images/i2c_protocol.jpg)

Note that, most I2C devices support repeated start condition. This means that before the communication ends with a stop condition, master device can repeat start condition with address byte and change the mode from writing to reading.

> ### Example of I2C communication
>
> **Question:** Let the following image shows several frames of I2C communication between ATmega328P and a slave device. What circuit is it and what information was sent over the bus?
>
> &nbsp;
> ![Temperature reception from DHT12 sensor](images/twi-dht12_temperature_decoded.png)
>
> **Answer:** This communication example contains a total of five frames. After the start condition, which is initiated by the master, the address frame is always sent. It contains a 7-bit address of the slave device, supplemented by information on whether the data will be written to the slave or read from it to the master. The ninth bit of the address frame is an acknowledgment provided by the receiving side.
>
> Here, the address is 184 (decimal), i.e. `101_1100-0` in binary including R/W=0. The slave address is therefore 101_1100 (0x5c) and master will write data to the slave. The slave has acknowledged the address reception, so that the communication can continue.
>
> According to the list of [I2C addresses](https://learn.adafruit.com/i2c-addresses/the-list) the device could be humidity/temp or pressure sensor. The signals were really recorded when communicating with the humidity and temperature sensor.
>
> The data frame always follows the address one and contains eight data bits from the MSB to the LSB and is again terminated by an acknowledgment from the receiving side. Here, number `2` was written to the sensor. According to the [DHT12 sensor manual](../manuals/dht12_manual.pdf), this is the address of register, to which the integer part of measured temperature is stored. (The following register contains its decimal part.)
>
> | **Memory location** | **Description** |
> | :-: | :-- |
> | 0x00 | Humidity integer part |
> | 0x01 | Humidity decimal part |
> | 0x02 | Temperature integer part |
> | 0x03 | Temperature decimal part |
> | 0x04 | Checksum |
>
> After the repeated start, the same circuit address is sent on the I2C bus, but this time with the read bit R/W=1 (185, `101_1100_1`). Subsequently, data frames are sent from the slave to the master until the last of them is confirmed by the NACK value. Then the master generates a stop condition on the bus and the communication is terminated.
>
> The communication in the picture therefore records the temperature transfer from the sensor, when the measured temperature is 25.3 degrees Celsius.
>
> | **Frame #** | **Description** |
> | :-: | :-- |
> | 1 | Address frame with SLA+W = 184 (0x5c<<1 + 0) |
> | 2 | Data frame sent to the Slave represents the ID of internal register |
> | 3 | Address frame with SLA+R = 185 (0x5c<<1 + 1) |
> | 4 | Data frame with integer part of temperature read from Slave |
> | 5 | Data frame with decimal part of temperature read from Slave |

<a name="part2"></a>

## Part 2: I2C scanner

The goal of this task is to find all devices connected to the I2C bus.

1. Use breadboard, jumper wires, and connect I2C devices to ESP32 GPIO pins.

   > **Note:** Connect the components on the breadboard only when the supply voltage/USB is disconnected! There is no need to connect external pull-up resistors on the SDA and SCL pins, because the internal ones are used.

   ![schema_i2c](images/schema_i2c.png)

   * SH1106 I2C [OLED display](https://randomnerdtutorials.com/esp32-ssd1306-oled-display-arduino-ide/) 128x64

   * Combined module with [RTC DS3231](../manuals/ds3231_manual.pdf) (Real Time Clock) and [AT24C32](../manuals/at24c32_manual.pdf) EEPROM memory

   * Optional: Humidity/temperature [DHT12](../manuals/dht12_manual.pdf) digital sensor

   * Optional: Humidity/temperature/pressure [BME280](https://cdn-shop.adafruit.com/datasheets/BST-BME280_DS001-10.pdf) sensor

   * Optional: [GY-521 module](../manuals/mpu-6050_datasheet.pdf) (MPU-6050 Microelectromechanical systems that features a 3-axis gyroscope, a 3-axis accelerometer, a digital motion processor (DMP), and a temperature sensor).

2. Ensure your ESP32 board is connected to your computer via a USB cable. Open the Thonny IDE and set the interpreter to `ESP32`. You can click the red **Stop/Restart** button or press the on-board reset button if necessary to reset the board.

3. Create a new file `i2c_scan.py` in Thonny and perform a scan to detect the slave addresses of connected I2C devices. Endeavor to determine the corresponding device associated with each address.

   ```python
   from machine import I2C
   from machine import Pin

   # Init I2C using pins GP22 & GP21 (default I2C0 pins)
   i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

   print("Scanning I2C... ", end="")
   addrs = i2c.scan()
   print(f"{len(addrs)} device(s) detected")

   for addr in addrs:
       print(f"{addr}\t {hex(addr)}")
   ```

<a name="part3"></a>

## Part 3: Communication with I2C devices

1. Create a new script file `i2c_rtc.py` and read data from RTC DS3231 (Real Time Clock) I2C device. Note that, according to the [DS3231 manual](../manuals/ds3231_manual.pdf), the RTC memory has the following structure.

   ![rtc_regs](images/rtc_registers.png)

   Use the following code to get hours, minutes, and seconds stored in three bytes, starting at address 0.

   ```python
   from machine import Pin, I2C
   import time

   SLA_ADDR = ...  # Get the address from the previous task

   # Init I2C using pins GP22 & GP21 (default I2C0 pins)
   i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)

   # Check the sensor
   addrs = i2c.scan()
   if SLA_ADDR not in addrs:
       raise Exception(f"`{hex(SLA_ADDR)}` is not detected")

   print(f"I2C configuration : {str(i2c)}")
   print("Start using I2C. Press `Ctrl+C` to stop")

   try:
       # Forever loop
       while True:
           # From `SLA_ADDR` device, read 3 bytes, starting at address 0
           val = i2c.readfrom_mem(SLA_ADDR, 0, 3)

           # PRINT THE TIME FROM RTC

           time.sleep(1)

   except KeyboardInterrupt:
       # This part runs when Ctrl+C is pressed
       print("Program stopped. Exiting...")

       # Optional cleanup code
   ```

2. Use the MicroPython manual and find the description of the following methods from [I2C class](https://docs.micropython.org/en/latest/library/machine.I2C.html):

   * `I2C.scan()`
   * `I2C.readfrom()`
   * `I2C.readfrom_into()`
   * `I2C.writeto()`
   * `I2C.writevto()`
   * `I2C.readfrom_mem()`
   * `I2C.readfrom_mem_into()`
   * `I2C.writeto_mem()`

   Modify your code and set the initial (correct) time to RTC device first.

3. Connect the logic analyzer to the I2C bus wires (SCL and SDA) between the microcontroller and the sensor. Launch the logic analyzer software Logic and **Start** the capture. Saleae Logic software offers a decoding feature to transform the captured signals into meaningful I2C messages. Click to **+ button** in **Analyzers** part and setup **I2C** decoder.

   > **Note:** To perform this analysis, you will need a logic analyzer such as [Saleae](https://www.saleae.com/) or [similar](https://www.amazon.com/KeeYees-Analyzer-Device-Channel-Arduino/dp/B07K6HXDH1/ref=sr_1_6?keywords=saleae+logic+analyzer&qid=1667214875&qu=eyJxc2MiOiI0LjIyIiwicXNhIjoiMy45NSIsInFzcCI6IjMuMDMifQ%3D%3D&sprefix=saleae+%2Caps%2C169&sr=8-6) device. Additionally, you should download and install the [Saleae Logic](https://www.saleae.com/pages/downloads) software on your computer.
   >
   > You can find a comprehensive tutorial on utilizing a logic analyzer in this [video](https://www.youtube.com/watch?v=CE4-T53Bhu0).

<a name="part4"></a>

## Part 4: OLED display 128x64

An OLED I2C display, or OLED I2C screen, is a type of display technology that combines an OLED (Organic Light Emitting Diode) panel with an I2C (Inter-Integrated Circuit) interface for communication. The I2C interface simplifies the connection between the display and a microcontroller, making it easier to control and integrate into various electronic projects.

1. Create a new file `sh1106.py`, consinsting the class for OLED display with SH1106 driver and copy/paste [the code](../modules/sh1106.py) to it. To import and use the class, the copy of file must be stored in the ESP32 device.

2. Create a new file `i2c_display.py` and write a script to print text on the display.

   ```python
   from machine import Pin, I2C
   from sh1106 import SH1106_I2C

   # Init I2C using pins GP22 & GP21 (default I2C0 pins)
   i2c = I2C(0, scl=Pin(22), sda=Pin(21), freq=100_000)
   print(f"I2C configuration : {str(i2c)}")

   # Init OLED display
   display = SH1106_I2C(i2c)

   # Add some text at (x, y)
   display.text("Using OLED and", 0, 40)
   display.text("ESP32", 50, 50)


   # WRITE YOUR CODE HERE


   # Finally update the OLED display so the text is displayed
   display.show()
   ```

3. Use other methods from `sh1106` [class](https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/) and draw lines and rectangles on the display. Here is the list of availabe methods for basic graphics.

   | **Method name** | **Description** | **Example** |
   | :-- | :-- | :-- |
   | `display.text(text, x, y)` | Display `text` at position `x`, `y` | `display.text("Using OLED...", 0, 0)` |
   | `display.pixel(x, y, color)` | Display one pixel at position. Optional `color`: 1 - visible, 0 - background color | `display.pixel(10, 20, 1)`
   | `display.hline(x, y, w, color)` | Horizontal line with width `w` and `color` | `display.hline(0, 64, 128, 1)` |
   | `display.vline(x, y, h, color)` | Vertical line with height `h` | `display.vline(9, 8, 22, 1)` |
   | `display.line(x1, y1, x2, y2, color)` | Diagonal line | `display.line(0, 0, 128, 64, 1)` |
   | `display.rect(x, y, w, h, color)` | Rectangle | `display.rect(0, 0, 128, 64, 1)` |
   | `display.fill_rect(x, y, w, h, color)` | Filled rectangle | `display.fill_rect(0, 0, 32, 32, 1)` |
   | `display.fill(color)` | Fill the whole screen (clear screen) | `display.fill(0)` |

4. Define a binary matrix, suggest your picture/icon, use the `display.pixel()` method, and print it on the display.

   ```python
   # Binary icon
   icon = [
       [0, 0, 0, 0, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 0, 0, 1, 1, 0],
       [1, 1, 1, 1, 0, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1],
       [1, 1, 1, 1, 1, 1, 1, 1, 1],
       [0, 1, 1, 1, 1, 1, 1, 1, 0],
       [0, 0, 1, 1, 1, 1, 1, 0, 0],
       [0, 0, 0, 1, 1, 1, 0, 0, 0],
       [0, 0, 0, 0, 1, 0, 0, 0, 0]]
   # Copy icon to OLED display position pixel-by-pixel
   pos_x, pos_y = 100, 50
   for j, row in enumerate(icon):
       for i, val in enumerate(row):
           display.pixel(i+pos_x, j+pos_y, val) 
   ```

5. Combine RTC and OLED examples and print current time on OLED display.

<a name="challenges"></a>

## Challenges

1. Transform the output of the I2C scanner application into a hexadecimal table format, as illustrated in the example below. Please be aware that the term `RA` signifies I2C addresses that are [reserved](https://www.pololu.com/file/download/UM10204.pdf?file_id=0J435) and not available for use with slave circuits.

   ```python
   Scanning I2C...

         .0 .1 .2 .3 .4 .5 .6 .7 .8 .9 .a .b .c .d .e .f
   0x0.: RA RA RA RA RA RA RA RA -- -- -- -- -- -- -- --
   0x1.: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   0x2.: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   0x3.: -- -- -- -- -- -- -- -- -- -- -- -- 3c -- -- --
   0x4.: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
   0x5.: -- -- -- -- -- -- -- 57 -- -- -- -- -- -- -- --
   0x6.: -- -- -- -- -- -- -- -- 68 -- -- -- -- -- -- --
   0x7.: -- -- -- -- -- -- -- -- RA RA RA RA RA RA RA RA
   
   3 device(s) detected
   ```

2. Read data from humidity/temperature DHT12 sensor. Note that, according to the [DHT12 manual](../manuals/dht12_manual.pdf), the internal DHT12 memory has the following structure.

   | **Memory location** | **Description** |
   | :-: | :-- |
   | 0x00 | Humidity integer part |
   | 0x01 | Humidity decimal part |
   | 0x02 | Temperature integer part |
   | 0x03 | Temperature decimal part |
   | 0x04 | Checksum |

3. Build an environmental monitoring system using an ESP32 board, I2C communication, and common sensors. The goal is to collect data on temperature, humidity, and air quality, and display this information on an OLED display.

4. Use BME280 sensor and read humidity, temperature and preassure values.

   * BME280 [class](../modules/bme280.py)
   * Testing [script](../solutions/06-serial/03-i2c_bme280.py)

<a name="references"></a>

## References

1. Ezoic. [I2C Info - I2C Bus, Interface and Protocol](https://i2c.info/)

2. Electronicshub.org. [Basics of I2C Communication | Hardware, Data Transfer, Configuration](https://www.electronicshub.org/basics-i2c-communication/)

3. MicroPython. [class I2C - a two-wire serial protocol](https://docs.micropython.org/en/latest/library/machine.I2C.html)

4. Adafruit. [List of I2C addresses](https://learn.adafruit.com/i2c-addresses/the-list)

5. Aosong. [Digital temperature DHT12](../manuals/dht12_manual.pdf)

6. NXP. [I2C-bus specification and user manual](https://www.pololu.com/file/download/UM10204.pdf?file_id=0J435)

7. Martin Fitzpatrick. [Driving I2C OLED displays with MicroPython](https://blog.martinfitzpatrick.com/oled-displays-i2c-micropython/)

8. Maxim Integrated. [DS3231, Extremely accurate I2C-Integrated RTC/TCXO/Crystal](../manuals/ds3231_manual.pdf)

9. LastMinuteEngineers. [Interface DS3231 Precision RTC Module with Arduino](https://lastminuteengineers.com/ds3231-rtc-arduino-tutorial/)
