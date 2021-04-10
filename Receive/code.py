import board
import adafruit_sdcard
import digitalio
import time
import busio
import adafruit_rfm9x
import storage
import os

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

while True:
    packet = rfm9x.receive(timeout=5.0) # Write down packet. Timeout of 5 seconds

    try: # Empty packet variable causes error in SD logging. Lazy fix is to use try / except
        with open("/sd/receiveLog.csv", "a") as f:
            led.value = True  # turn on LED to indicate we're writing to the file
            f.write(packet) # Log packet received to SD card
            time.sleep(0.1)
            led.value = False  # turn off LED to indicate we're done
            print(packet) # Print so we can see on serial monitor if we are using it

    except:
            pass # If there is an error... dont do anything

