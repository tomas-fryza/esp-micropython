# How to use MicroPython and ESP32/ESP8266

* [Wokwi simulator](#Wokwi-Simulator)
* [Installation](#Installation)
  * [ESP32](#ESP32)
  * [ESP8266](#ESP8266)
  * [Both](#Both)
* [How to use](#How-to-use)
  * [Thonny IDE](#Thonny-IDE)
  * [PyCharm IDE](#PyCharm-IDE)
  * [MicroPython Jupyter](#MicroPython-Jupyter)
* [Examples](#examples)
* [References](#References)

## Wokwi simulator

The easiest way to try MicroPython is in the [Wokwi](https://wokwi.com/micropython) online electronics simulator right in your web browser. You can use it to simulate Arduino, ESP32, STM32, and many other popular boards, parts and sensors in C, MicroPython or Rust.

## Installation

To use MicroPython with a real ESP32 board, you will need to follow these steps:

* Install MicroPython firmware
* Flash the firmware
* Connect to the Board's Serial REPL and interact with MicroPython
* Transfer files to the ESP32 board

There are several very good tutorials how to install and use MicroPython on an ESP microcontroller, such as [this one](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html) for Windows. The following text was tested under Linux-based operation system.

1. Install [Python](https://www.python.org/downloads/).

2. Open terminal (typically `Ctrl+Alt+T`) and install `esptool`:

    ```shell
    pip install esptool
    ```

    Connect your ESP board and test the [`esptool`](https://docs.espressif.com/projects/esptool/en/latest/esp32/esptool/basic-commands.html#):

    ```shell
    # Get the version
    esptool.py version

    # Read chip info, serial port, MAC address, and others
    # Note: Use `dmesg` command to find your USB port
    esptool.py --port /dev/ttyUSB0 flash_id

    # Read all eFuses from the chip
    espefuse.py --port /dev/ttyUSB0 summary
    ```

### ESP32

3. [Download](http://micropython.org/download/) the latest firmware for your target device, such as `esp32-20230426-v1.20.0.bin` for Espressif ESP32.

4. Erase flash of target device (use your port name):

    ```shell
    esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
    ```

5. Deploy the new firmware:

    ```shell
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
    ```

### ESP8266

3. [Download](https://micropython.org/download/esp8266/) the latest firmware, such as `esp8266-20230426-v1.20.0.bin`.

4. Erase the Flash before deploying the firmware:

    ```shell
    esptool.py --chip esp8266 --port /dev/ttyUSB0 erase_flash
    ```

5. Deploy the firmware:

    ```shell
    esptool.py --chip esp8266 --port /dev/ttyUSB0 write_flash --flash_mode dio --flash_size 4MB 0x0 esp8266-20230426-v1.20.0.bin
    ```

### Both

6. Test MicroPython via [PuTTY](https://putty.org/) or directly in terminal by `screen`. You need to press onboard reset button:

    ```shell
    screen /dev/ttyUSB0 115200 
    ```

    > **Note:** To exit the screen, press `Ctrl+A`, followed by `K` and `Y`.

    ```python
    >>> from machine import Pin
    
    # Display help for `Pin` class from `machine` package
    >>> help(Pin)

    # Check the LED pin on your board, usually it is `2`
    # Create output pin on GPIO2
    >>> led = Pin(2, Pin.OUT)
    >>> help(led)

    # Set pin to "on" (high) and "off" (low) levels
    >>> led.value(1)
    >>> led.value(0)

    >>> led(True)
    >>> led(False)

    >>> led.on()
    >>> led.off()
    ```

    Test some other useful commands from [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html):

    ```python
    # Get the current frequency of the CPU
    >>> import machine
    >>> machine.freq()

    # Get Flash size in Bytes
    >>> import esp
    >>> esp.flash_size()

    # Read the internal hall and temperature (in Fahrenheit) sensors
    >>> import esp32
    >>> esp32.hall_sensor()
    >>> esp32.raw_temperature()
    # FYI: temp_c = (temp_f-32.0) * (5/9)
    #      temp_f = temp_c * (9/5) + 32.0
    ```

## How to use

There are several IDEs (Integrated Development Environments) available for MicroPython programming, each with its own unique features and benefits. The most popular IDEs for MicroPython programming are:

* [Thonny](https://thonny.org/) is a popular IDE for MicroPython programming beginners. It has a simple and user-friendly interface and includes a MicroPython REPL (Read-Eval-Print Loop) that allows you to interact with the MicroPython interpreter and test your code in real-time. Thonny is free and open-source, and it runs on Windows, macOS, and Linux.

* [Mu](https://codewith.mu/) is another popular IDE for MicroPython programming that is designed for beginners. It has a built-in MicroPython REPL and includes a tool for flashing firmware onto your board. Mu is free and open-source, and it runs on Windows, macOS, and Linux.

* [PyCharm](https://www.jetbrains.com/pycharm/) is a powerful IDE that provides advanced features such as code completion, debugging, and version control integration. PyCharm also includes a MicroPython debugger that allows you to step through your code and set breakpoints. PyCharm is a commercial product, but has a Community Edition free version. It runs on Windows, macOS, and Linux.

* [Visual Studio Code](https://code.visualstudio.com/) is a popular and versatile IDE that supports multiple programming languages, including MicroPython. It provides many useful features such as syntax highlighting, code completion, and debugging. Visual Studio Code is free and open-source, and it runs on Windows, macOS, and Linux.

### Thonny IDE

1. Download and install Thonny IDE from [webpage](https://thonny.org/) or directly in terminal:

    ```shell
    sudo apt install thonny
    ```

2. Run the Thonny and select on-board interpreter. Go to **Run > Select interpreter...** and select `ESP32` or `ESP8266`. Test the [board](#Both) in **Shell**.

3. Copy/paste the [example blink](examples/01-blink/main.py) code and run the application by **Run > Run current script F5**.

### PyCharm IDE

In the next, the **PyCharm IDE** is used, mainly because it provides advanced features and can be especially helpful for larger and more complex Python/MicroPython projects.

1. Download and install [Community edition PyCharm](https://www.jetbrains.com/pycharm/download/).

2. Run the PyCharm and install MicroPython plugin for PyCharm. Go to **File > Settings > Plugins > Marketplace**, search for `MicroPython` and install it.

3. Create a new project, name and locate it wherever you want. Connect your ESP32/ESP8266 board vie USB.

4. Go to **File > Settings > Languages & Frameworks > MicroPython** and:
    -- check `Enable MicroPython support`
    -- select `ESP8266` device type (it works also for ESP32)
    -- set `Device path` for your board, such as `/dev/ttyUS0`

    Test [REPL](#Both) in **File > Tools > MicroPython > MicroPython REPL**.

5. Add a file to the project. Select **File > New... > Python file** and name it `main.py`. The missing packages will be installed to work with the ESP32/8266. Copy/paste the [example blink](examples/01-blink/main.py) code to `main.py` file.

6. Upload a program. Right-click the `main.py` file in the project browser on the left side and select **Run 'Flash main.py'**.

    > **Note:** Check [MicroPython Tutorial](http://mpy-tut.zoic.org/tut/input-and-output.html) for other simple examples and see description of [machine module](https://docs.micropython.org/en/latest/library/machine.html?highlight=machine).

## Examples

* [Blink](examples/01-blink/main.py)
* [Wi-Fi scan](examples/03-wifi-scan/main.py)
* [Wi-Fi connection](examples/04-wifi-connection/main.py)

## TODO

* [ ] Howto Use MicroPython in Jupyter
* [ ] MicroPython Programming Basics, https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/
* [ ] Example: Button, LED, PWM, https://randomnerdtutorials.com/micropython-gpios-esp32-esp8266/
* [x] Example: Wi-Fi scan
* [x] Example: Connect to a Wi-Fi
* [ ] Example: I2C sensor, https://randomnerdtutorials.com/esp32-esp8266-dht11-dht22-micropython-temperature-humidity-sensor/
* [ ] Example: Simple web server, https://randomnerdtutorials.com/esp32-esp8266-micropython-web-server/
* [ ] Example: Sensor + Wi-Fi + Cloud
* [ ] Example: Sensor + Wi-Fi + smart phone, https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
* [ ] Example: Relay + Wi-Fi server + smart phone, https://randomnerdtutorials.com/micropython-relay-module-esp32-esp8266/
* [ ] Example: Bluetooth
* [ ] Howto Use MicroPython on ESP32-CAM

> - [ ] Online tool: [https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/](https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/)
> - [ ] Rts/Dtr handshake signals must be disabled?!
> - [ ] [https://forum.micropython.org/viewtopic.php?t=10151&start=10](https://forum.micropython.org/viewtopic.php?t=10151&start=10)

## References

1. [How to install MicroPython on an ESP32 microcontroller ](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html)

2. [Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

3. [Video tutorial about ESP32 MicroPython](https://www.youtube.com/playlist?list=PLw0SimokefZ3uWQoRsyf-gKNSs4Td-0k6)

4. [Web Serial ESPTool (in Chrome)](https://learn.adafruit.com/adafruit-magtag/web-serial-esptool)

5. [Getting Started with the MicroPython in PyCharm for Raspberry Pi Pico](https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/getting-started-with-the-micropython-in-pycharm-for-raspberry-pi-pico)

6. [Jupyter MicroPython Kernel](https://github.com/goatchurchprime/jupyter_micropython_kernel/tree/master)

7. [MicroPython: Programming an ESP using Jupyter Notebook](https://lemariva.com/blog/2019/01/micropython-programming-an-esp-using-jupyter-notebook)

8. MicroPython Documentation. [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html)

9. [40+ MicroPython Projects, Tutorial and Guides with ESP32 / ESP8266](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)
