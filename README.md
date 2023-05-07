# How to use MicroPython and ESP32/ESP8266

There are several very good tutorials how to instanll and use MicroPython on an ESP microcontroller, such as [this one for Windows](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html). The following text was tested under Linux-based operation system.

1. Install [Python](https://www.python.org/downloads/).

2. Open terminal (typically `Ctrl+Alt+T`) and install `esptool`:

    ```shell
    pip install esptool
    ```

  Connect your ESP board and test the `esptool`:

  ```shell
  # Get the version
  esptool.py version

  # Read flash chip manufacturer name, port, and other usefull info
  esptool.py flash_id

  espefuse.py --port /dev/ttyUSB0 summary
  ```

## ESP32

1. [Download MicroPython](http://micropython.org/download/) for target device. For Espressif ESP32, the latest version is [esp32-20230426-v1.20.0.bin](https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin).

2. Erase flash of target device (use your port name):

  ```shell
  esptool.py --chip eps32 --port /dev/ttyUSB0 erase_flash
  ```

3. Deploy the new firmware:

  ```shell
  esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
  ```

4. Test it via [PuTTY](https://putty.org/) or directly in terminal by `screen`. You need to press the reset button:

  ```shaell
  screen /dev/ttyUSB0 115200 
  ```

  > **Note:** To exit the screen, press `Ctrl+A`, followed by `K` and `Y`.

  ```python
  >>> from machine import Pin

  # Check the LED pin on your board, usually it is `2`
  >>> led = Pin(2, Pin.OUT)
  >>> led.value(1)
  >>> led.value(0)
  >>> led(True)
  >>> led(False)
  >>> led.on()
  >>> led.off()
  ```

## ESP8266

1. [Download the firmware](https://micropython.org/download/esp8266/)

2. Erase the Flash:
    
  ```shell
  esptool.py --chip eps8266 --port /dev/ttyUSB0 erase_flash
  ```
    
3. Deploy the firmware:
    
  ```shell
  esptool.py -chip esp8266 --port /dev/ttyUSB0 write_flash --flash_mode dio --flash_size 4MB 0x0 esp8266-20230426-v1.20.0.bin
  ```

## ESP32-CAM

- [ ] Online tool: [https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/](https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/)
- [ ] Rts/Dtr handshake signals must be disabled?!

  ```shell
  monitor_rts = 0
  monitor_dtr = 0
  ```

- [ ] [https://forum.micropython.org/viewtopic.php?t=10151&start=10](https://forum.micropython.org/viewtopic.php?t=10151&start=10)

### References

1. [How to install MicroPython on an ESP32 microcontroller ](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html)

2. [Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

3. [Video tutorial about ESP32 MicroPython](https://www.youtube.com/playlist?list=PLw0SimokefZ3uWQoRsyf-gKNSs4Td-0k6)

4. [Web Serial ESPTool] (in Chrome)(https://learn.adafruit.com/adafruit-magtag/web-serial-esptool)

5. [PyCharm](https://www.youtube.com/watch?v=nnKyBhFzTmk)
