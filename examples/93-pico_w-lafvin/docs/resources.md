
https://lafvin-pico-development-kit.readthedocs.io/en/latest/about_this_kit.html

https://github.com/lafvintech/LAFVIN-PICO-Development-Kit

## Hardware Specifications

### Display Parameters
* Resolution: 320x480 pixels
* Display Driver IC: ST7796U
* Operating Voltage: 3.3V 
* Touch Type: Capacitive Touch Screen (GT911)
* Display Communication Protocol: SPI (SPI0)
* Touch Screen Communication Protocol: I2C (I2C0 SDA: GP8, SCL: GP9)

### Pin Assignment
* GP2-GP7, GP10-GP11: SPI0 connected to TFT screen
* GP8-GP9: I2C0 connected to touch screen
* GP12: RGB LED (WS2812)
* GP13: Buzzer
* GP14-GP15: Buttons (BTN2, BTN1)
* GP16-GP17: LED indicators (D1, D2)
* GP26-GP27: Joystick (ADC0 X-axis, ADC1 Y-axis)

### TFT Display Pinout
| Raspberry Pi Pico | 3.5" TFT Screen |
|---|---|
| GP2 | CLK |
| GP3 | MOSI |
| GP4 | MISO |
| GP5 | CS |
| GP6 | DC |
| GP7 | RST |
| GP10 | TPRST |
| GP11 | TPINT |

### Capacitive Touch Screen Pinout
| Raspberry Pi Pico | Capacitive Touch Screen |
|---|---|
| I2C0 SDA GP8 | SDA |
| I2C0 SCL GP9 | SCL |


Display:

https://coxxect.blogspot.com/2025/02/use-st7796-spi-lcd-on.html
