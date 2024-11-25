# This example makes two LEDs blink at different intervals,
# showcasing how `asyncio` can handle multiple tasks concurrently
# without blocking the execution of other task(s).
#
# See:
# https://docs.micropython.org/en/latest/library/asyncio.html
# https://bbc.github.io/cloudfit-public-docs/asyncio/asyncio-part-2.html
# https://gpiocc.github.io/learn/micropython/esp/2020/06/13/martin-ku-asynchronous-programming-with-uasyncio-in-micropython.html
# https://randomnerdtutorials.com/micropython-esp32-esp8266-asynchronous-programming/

import asyncio

async def blink(led, period_ms):
    while True:
        print(f"[{led}] loop start")
        led.on()
        print(f"[{led}] on")
        await asyncio.sleep_ms(20)  # Non-blocking delay
        led.off()
        print(f"[{led}] off")
        await asyncio.sleep_ms(period_ms)

async def main():
    t1 = asyncio.create_task(blink(led1, 700))
    t2 = asyncio.create_task(blink(led2, 400))
    print(t1)
    print(t2)
    await asyncio.sleep_ms(5_000)
    
from machine import Pin

led1 = Pin(2, Pin.OUT)
led2 = Pin(5, Pin.OUT)

asyncio.run(main())
