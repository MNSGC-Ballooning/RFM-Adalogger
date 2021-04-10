import board
import adafruit_sdcard
import digitalio
import time
import busio
import adafruit_rfm9x
import storage
import os
import microcontroller

# declare SPI communication instance
spi = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)

#declare SPI pins specific to the RFM shield
cs = digitalio.DigitalInOut(board.D10)
reset = digitalio.DigitalInOut(board.D11)

# declare rfm instance
rfm9x = adafruit_rfm9x.RFM9x(spi, cs, reset, 433.0)

# declare SPI pins specific to SD card (CS pin is written on bottom of feather adalogger board)
csSD = digitalio.DigitalInOut(board.D4)
sdcard = adafruit_sdcard.SDCard(spi, csSD)

# Init SD card
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Init onboard LED
led = digitalio.DigitalInOut(board.D13)
led.direction = digitalio.Direction.OUTPUT

# Variable to increment how many times we have looped so we can see which packets are lost
counter = 0

# File header each time board is rebooted
header = "Temperature (C), Seconds Since Bootup, Increment Packet \n"
with open("/sd/myLog.csv", "a") as f:
    f.write(header)

# Transmit file header - why not?
rfm9x.send(header)

while True:

    counter = counter + 1 # increment counter

    with open("/sd/myLog.csv", "a") as f:
        led.value = True  # turn on LED to indicate we're writing to the file
        t = microcontroller.cpu.temperature # Find temperature of chip
        String = "%0.1f, " % t + "%0.3f," % time.monotonic() + "%d \n" % counter
        f.write(String) # Log values to SD card
        time.sleep(0.1)
        led.value = False  # turn off LED to indicate we're done
        print(String) # Print data to serial monitor when using

    rfm9x.send(String) # Transmit packet
    time.sleep(0.9)