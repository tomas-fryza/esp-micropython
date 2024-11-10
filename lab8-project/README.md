# Project

## Instructions

*The goal of this project is for small teams of 3-4 students to explore a chosen topic, use the [labs's components](https://github.com/tomas-fryza/esp-micropython?tab=readme-ov-file#components-and-tools), develop solutions, simulate and implement them, create documentation, and present the results. Team members will organize and divide tasks among themselves.*

* The students will work on the project for four weeks, ending with a presentation and a practical demonstration (simulations alone are not enough), see the course schedule in e-learning.

* The ESP32 code must be written in MicroPython and must be implementable on an ESP32 FireBeetle board.

* If needed, use the simulation tools, such as [wokwi](https://wokwi.com/), [Falstad](https://www.falstad.com/circuit/circuitjs.html), etc.

* Draw illustrative flowcharts for all important functions/interrupt routines.

* Design a block diagram or circuit diagram of your application (EasyEDA, KiCAD, Eagle, ...).

* Optionally, design a PCB and/or 3D-printable enclosure for your solution.

* Use modules from the labs. Create own modules (and documentation) for the new components.

* Follow coding standards in your codes.

* Strictly follow licenses for third-party libraries !

* Create a public [GitHub](https://github.com/) (or any other online software development platform) repository for your project and publish all files here.

* Provide a list of all tools used during the project, including Machine Learning (some are listed [here](https://github.com/tomas-fryza/esp-micropython/wiki)).

* A PowerPoint-style presentation is not required; a good `README.md` on GitHub is sufficient.

* During the presentation, you can play a short video (max 1 minute) with subtitles or explanatory captions.

# Recommended README.md file structure

### Team members

* Member 1 (responsible for ...)
* Member 2 (responsible for ...)
* Member 3 (responsible for ...)

## Hardware description

Describe your implementation and include block or circuit diagram(s).

## Software description

Include flowcharts of your algorithm(s) and direct links to the source files. Present the modules you used in the project.

## Instructions and photos

Describe how to use the application. Add photos or videos of your application.

## References and tools

1. Put here the references and online tools you used.
2. ...

# MPA-DIE topic 2024/25

Complete the free online course at coursera.org by Edge Impulse [Introduction to Embedded Machine Learning](https://www.coursera.org/learn/introduction-to-embedded-machine-learning)

Solve a machine learning project using the ESP32 or your Smart phone and [Edge Impulse tool](https://edgeimpulse.com/).

# BPA-DE2 topics 2024/25

### Measurement/Control/Visualization of the environment for tropical plants

The goal of the project would be to create a system that measures key environmental parameters (such as temperature, humidity, light levels, soil moisture) for tropical plants. This system should also allow the user to control or adjust environmental conditions and visualize the data.

Inspiration:
* [Climate Chamber System](https://projecthub.arduino.cc/ms_peach/climate-chamber-system-c545de)

Possible components:
* Plant terrarium
* I2C temperature and humidity sensor
* Photoresistor
* Soil moisture sensor
* OLED display
* RGB LED strip Neopixel WS2812B
* Relays
* Brushless DC fan, NMOS transistor
* ESP8266 Wi-Fi module

### GPS tracker

(*Max 2 teams.*)

A GPS-based environmental sensor data logger that integrates GPS functionality for location tracking along with environmental sensor(s) to monitor and log environmental conditions. The system captures and stores sensor data such as temperature, humidity, air quality, or other relevant environmental metrics. The logged data, along with its corresponding location information, can be displayed and exported for further analysis. The project aims to provide real-time monitoring, data storage, and export capabilities.

Possible components:
* GPS module
* I2C temperature, humidity sensor, and presure sensor
* Photoresistor
* air quality sensors
* OLED display

### Digital clock

(*Max 2 teams.*)

Design and implement a digital clock using NeoPixel displays. The clock will display the current time, support alarms, and synchronize with network time servers (NTP) to ensure accurate timekeeping. Set up physical buttons or touch/proximity input to interact with the clock (e.g., set time, set alarms, snooze alarms). Implement basic functions to control the NeoPixel LEDs (e.g., setting color, brightness, and individual pixel control).

Optional updates:
* In addition to the standard digital time display, implement a mode that shows time in binary format. You can display each digit (hour, minute, second) in binary using a set of LEDs, where each LED represents a bit (0 or 1). This could be a cool and educational feature.
* Integrate a temperature/humidity sensor to measure indoor temperature.
* Implement an automatic night mode that reduces the display brightness in low-light conditions or based on a set schedule.
* Implement a feature that allows the clock to display time in multiple time zones.

Possible components:
* [NeoPixel displays](https://www.vokolo.cz/rubriky/navody/navod-na-stavbu-hodin-neopixsegment/)
* RGB LED strip Neopixel WS2812B
* I2C temperature and humidity sensor
* Photoresistor

### ESP-NOW mesh network with ESP32

ESP-NOW is a wireless communication protocol developed by Espressif for low-power, peer-to-peer communication between ESP32 devices. It allows multiple ESP32 boards to communicate directly with each other without the need for a Wi-Fi router, making it ideal for applications where low-latency and energy efficiency are important. In this project, ESP-NOW can be used to enable real-time data exchange between two or more devices, such as synchronizing a digital clock across multiple locations or sending sensor data between a master and slave device.
