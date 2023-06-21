# How to use MicroPython and ESP32/ESP8266

* [Wokwi simulator](#Wokwi-Simulator)
* [MicroPython installation](#MicroPython-installation)
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

   ![wokwi_blink](images/wokwi_blink.png)

## MicroPython installation

To use MicroPython with a real ESP32 board, you will need to follow these steps:

* Download MicroPython firmware
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
    >>> print("Hi there!")
    Hi there!

    # Operators used for the different functions like division,
    # multiply, addition and subtraction
    >>> 10/3
    3.333333
    >>> 10//3
    3
    >>> 10%3
    1
    >>> 10*3
    30
    >>> 10**3
    1000
    
    # Integers, floats, strings
    >>> type(10)
    <class 'int'>
    >>> type(10.0)
    <class 'float'>

    >>> pi = 3.1415
    >>> pi_str = str(pi)
    >>> type(pi_str)
    <class 'str'>
    >>> len(pi_str)
    6

    # `ord` returns unicode code of a specified character
    >>> ord("A")
    65
    >>> ord("a")
    97
    >>> ord("0")
    48

    >>> print(pi_str)
    3.1415
    >>> ord(pi_str[0])
    51
    >>> ord(pi_str[-1])
    53
    ```

    See MicroPython tutorials, such as [MicroPython Programming Basics with ESP32 and ESP8266](https://randomnerdtutorials.com/micropython-programming-basics-esp32-esp8266/) for detailed explanation.

    Test some other useful commands from [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html):

    ```python
    >>> import sys
    >>> sys.platform
    'esp32'

    # Get the current frequency of the CPU and RTC time
    >>> import machine
    >>> help(machine)
    >>> machine.freq()
    >>> machine.RTC().datetime()

    # Get Flash size in Bytes
    >>> import esp
    >>> esp.flash_size()

    # Read the internal temperature (in Fahrenheit)
    >>> import esp32
    >>> esp32.raw_temperature()
    # FYI: temp_c = (temp_f-32) * (5/9)
    #      temp_f = temp_c * (9/5) + 32
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

   ![thonny_blink](images/thonny_blink.png)

### PyCharm IDE

In the next, the **PyCharm IDE** is used, mainly because it provides advanced features and can be especially helpful for larger and more complex Python/MicroPython projects.

1. Download and install [Community edition PyCharm](https://www.jetbrains.com/pycharm/download/).

2. Run the PyCharm and install MicroPython plugin for PyCharm. Go to **File > Settings > Plugins > Marketplace**, search for `MicroPython` and install it.

3. Create a new project, name and locate it wherever you want. Connect your ESP32/ESP8266 board vie USB.

4. Go to **File > Settings > Languages & Frameworks > MicroPython** and:
    -- check `Enable MicroPython support`
    -- select `ESP8266` device type (it works also for ESP32)
    -- set `Device path` for your board, such as `/dev/ttyUS0`
    -- click on `OK` button

    Test [REPL](#Both) in **File > Tools > MicroPython > MicroPython REPL Alt+Shift+R**. Press on-board reset button if necesary.

    > **Note:** Sometimes, there is a useful function to clear all files store in device's memory. Select **File > Tools > MicroPython > Remove All Files from MicroPython Device**.

5. Add a file to the project. Select **File > New... > Python file** and name it `main.py`. The missing packages will be installed to work with the ESP32/8266. Copy/paste the [example blink](examples/01-blink/main.py) code to `main.py` file.

6. Upload a program. Right-click the `main.py` file in the project browser on the left side and select **Run 'Flash main.py'**.

   ![pycharm_blink](images/pycharm_blink.png)

    > **Note:** Check [MicroPython Tutorial](http://mpy-tut.zoic.org/tut/input-and-output.html) for other simple examples and see description of [machine module](https://docs.micropython.org/en/latest/library/machine.html?highlight=machine).

## Examples

* [Blink](examples/01-blink/main.py)
* [Wi-Fi scan](examples/03-wifi-scan/main.py)
* [Wi-Fi connection](examples/04-wifi-connection/main.py)
* [I2C humidity & temperature sensor](examples/05-i2c-sensor/main.py)
* [I2C sensor & ThingSpeak](examples/06-i2c-sensor-thingspeak/main.py)
* [RTC & NTP times](examples/07-rtc/main.py)
* [Wi-Fi access point](examples/08-access-point/boot.py)

## Useful information

* [ESP32 brief overview](https://www.youtube.com/watch?v=DoctWoxIaH8) (YouTube video)
* [FireBeetle board](docs/firebeetle.md)

## TODO

* [ ] Example: Sensor + Wi-Fi + smart phone, https://randomnerdtutorials.com/micropython-esp32-esp8266-dht11-dht22-web-server/
* [ ] Howto Use MicroPython in Jupyter
* [ ] Example for Wokwi: Button, LED, Relay
* [ ] Example: Bluetooth
* [ ] Example: Timers, interrupts
* [ ] Example: Deep sleep
* [ ] Howto Use MicroPython on ESP32-CAM

> - [ ] Online tool: [https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/](https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/)
> - [ ] Rts/Dtr handshake signals must be disabled?!
> - [ ] [https://forum.micropython.org/viewtopic.php?t=10151&start=10](https://forum.micropython.org/viewtopic.php?t=10151&start=10)

## References

1. [How to install MicroPython on an ESP32 microcontroller](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html)

2. [Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

3. [Video tutorial about ESP32 MicroPython](https://www.youtube.com/playlist?list=PLw0SimokefZ3uWQoRsyf-gKNSs4Td-0k6)

4. [Web Serial ESPTool (in Chrome)](https://learn.adafruit.com/adafruit-magtag/web-serial-esptool)

5. [Getting Started with the MicroPython in PyCharm for Raspberry Pi Pico](https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/getting-started-with-the-micropython-in-pycharm-for-raspberry-pi-pico)

6. [Jupyter MicroPython Kernel](https://github.com/goatchurchprime/jupyter_micropython_kernel/tree/master)

7. [MicroPython: Programming an ESP using Jupyter Notebook](https://lemariva.com/blog/2019/01/micropython-programming-an-esp-using-jupyter-notebook)

8. MicroPython Documentation. [Quick reference for the ESP32](https://docs.micropython.org/en/latest/esp32/quickref.html)

9. [40+ MicroPython Projects, Tutorial and Guides with ESP32 / ESP8266](https://randomnerdtutorials.com/projects-esp32-esp8266-micropython/)
