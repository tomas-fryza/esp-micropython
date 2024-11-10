.. MicroPython Examples documentation master file, created by
   sphinx-quickstart on Sun Nov 10 14:04:56 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to MicroPython course's documentation!
==============================================

:Release: |release|
:Date: |today|

General documentation
---------------------

This section covers the basic setup and installation steps for getting started with MicroPython.

.. toctree::
   :maxdepth: 2

   installation

Modules
-------

This section covers all the key modules used in the MicroPython course.

- **Basic I/O components**: Learn about the essential I/O modules in MicroPython.
- **HD44780-based LCD**: Documentation on controlling an HD44780-based LCD.
- **SH1106-based OLED**: Instructions for using an SH1106-based OLED display.
- **DHT12 sensor**: Learn how to interface with the DHT12 temperature and humidity sensor.
- **BME280 sensor**: Documentation on using the BME280 sensor for temperature, humidity, and pressure readings.
- **Wi-Fi**: How to connect and interact with Wi-Fi networks using MicroPython.

Each of the topics above is explained in more detail in the following sections.

.. toctree::
   :maxdepth: 1

   modules/hw_config
   modules/lcd
   modules/oled
   modules/dht12
   modules/bme280
   modules/wifi
