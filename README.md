# How to use MicroPython and ESP32/ESP8266

* [Installation](#Installation)
  * [ESP32](#ESP32)
  * [ESP8266](#ESP8266)
* [IDEs](#IDEs)
* [MicroPython Jupyter](#MicroPython-Jupyter)
* [References](#References)

## Installation

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

3. [Download MicroPython](http://micropython.org/download/) for target device. For Espressif ESP32, the latest version is [esp32-20230426-v1.20.0.bin](https://micropython.org/resources/firmware/esp32-20230426-v1.20.0.bin).

4. Erase flash of target device (use your port name):

    ```shell
    esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
    ```

5. Deploy the new firmware:

    ```shell
    esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 esp32-20230426-v1.20.0.bin
    ```

6. Test it via [PuTTY](https://putty.org/) or directly in terminal by `screen`. You need to press the reset button:

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

> TODO: ESP32-CAM
>
> - [ ] Online tool: [https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/](https://rafaelaroca.wordpress.com/2021/07/15/esp32-camera-micropython-and-no-esptool/)
> - [ ] Rts/Dtr handshake signals must be disabled?!
> - [ ] [https://forum.micropython.org/viewtopic.php?t=10151&start=10](https://forum.micropython.org/viewtopic.php?t=10151&start=10)

## IDEs

There are several IDEs (Integrated Development Environments) available for MicroPython programming, each with its own unique features and benefits. The most popular IDEs for MicroPython programming are:

* [Thonny](https://thonny.org/) is a popular IDE for MicroPython programming beginners. It has a simple and user-friendly interface and includes a MicroPython REPL (Read-Eval-Print Loop) that allows you to interact with the MicroPython interpreter and test your code in real-time. Thonny is free and open-source, and it runs on Windows, macOS, and Linux.

* [Mu](https://codewith.mu/) is another popular IDE for MicroPython programming that is designed for beginners. It has a built-in MicroPython REPL and includes a tool for flashing firmware onto your board. Mu is free and open-source, and it runs on Windows, macOS, and Linux.

* [PyCharm](https://www.jetbrains.com/pycharm/) is a powerful IDE that provides advanced features such as code completion, debugging, and version control integration. PyCharm also includes a MicroPython debugger that allows you to step through your code and set breakpoints. PyCharm is a commercial product, but has a Community Edition free version. It runs on Windows, macOS, and Linux.

* [Visual Studio Code](https://code.visualstudio.com/) is a popular and versatile IDE that supports multiple programming languages, including MicroPython. It provides many useful features such as syntax highlighting, code completion, and debugging. Visual Studio Code is free and open-source, and it runs on Windows, macOS, and Linux.

In the next, the **PyCharm IDE** is used, mainly because it provides advanced features and can be especially helpful for larger and more complex Python/MicroPython projects.

1. Download and install [Community edition PyCharm](https://www.jetbrains.com/pycharm/download/).

2. Run the PyCharm and install MicroPython plugin for PyCharm. Go to **File > Settings > Plugins > Marketplace**, search for `MicroPython` and install it.

3. Create a new project, name and locate it wherever you want. Connect your ESP32/ESP8266 board vie USB.

4. Go to **File > Settings > Languages & Frameworks > MicroPython** and:
    -- check `Enable MicroPython support`
    -- select `ESP8266` device type (it works also for ESP32)
    -- set `Device path` for your board, such as `/dev/ttyUS0`

    Test REPL in **File > Tools > MicroPython > MicroPython REPL**:

    ```python
    >>> from machine import Pin

    # Check the LED pin on your board, usually it is `2`
    >>> led = Pin(2, Pin.OUT)
    >>> led.on()
    >>> led.off()
    ```

5. Add a file to the project. Select **File > New... > Python file** and name it `main.py`. The missing packages will be installed to work with the ESP32/8266. Copy/paste the following code to `main.py` file:

    ```python
    from machine import Pin
    from time import sleep

    PIN_LED = 2


    def main():
        led = Pin(PIN_LED, Pin.OUT)

        while True:
            led.value(1)
            sleep(0.75)
            led(False)
            sleep(0.25)


    if __name__ == "__main__":
        main()
    ````

6. Upload a program. Right-click the `main.py` file in the project browser on the left side and select **Run 'Flash main.py'**.

    > **Note:** Check [MicroPython Tutorial](http://mpy-tut.zoic.org/tut/input-and-output.html) for other simple examples and see description of [machine module](https://docs.micropython.org/en/latest/library/machine.html?highlight=machine).

## MicroPython Jupyter

TBD

## References

1. [How to install MicroPython on an ESP32 microcontroller ](https://pythonforundergradengineers.com/how-to-install-micropython-on-an-esp32.html)

2. [Getting started with MicroPython on the ESP32](https://docs.micropython.org/en/latest/esp32/tutorial/intro.html)

3. [Video tutorial about ESP32 MicroPython](https://www.youtube.com/playlist?list=PLw0SimokefZ3uWQoRsyf-gKNSs4Td-0k6)

4. [Web Serial ESPTool] (in Chrome)(https://learn.adafruit.com/adafruit-magtag/web-serial-esptool)

5. [Getting Started with the MicroPython in PyCharm for Raspberry Pi Pico](https://community.element14.com/products/raspberry-pi/raspberrypi_projects/b/blog/posts/getting-started-with-the-micropython-in-pycharm-for-raspberry-pi-pico)

6. Video tutorial: [How to Get Started with MicroPython](https://www.youtube.com/watch?v=elBtWZ_fOZU&list=PLw0SimokefZ3uWQoRsyf-gKNSs4Td-0k6)

7. https://github.com/goatchurchprime/jupyter_micropython_kernel/tree/master

8. https://lemariva.com/blog/2019/01/micropython-programming-an-esp-using-jupyter-notebook
