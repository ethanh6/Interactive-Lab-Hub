import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import webcolors, os
from adafruit_rgb_display.rgb import color565
from datetime import datetime, timezone

# Configuration for CS and DC pins (these are FeatherWing defaults on M0/M4):
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None

# Config for display baudrate (default max is 24mhz):
BAUDRATE = 64000000

# Setup SPI bus using hardware SPI:
spi = board.SPI()

# Create the ST7789 display:
disp = st7789.ST7789(
    spi,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40,
)



# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for full color.
height = disp.width  # we swap height/width to rotate it to landscape!
width = disp.height
image = Image.new("RGB", (width, height))
rotation = 90

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
disp.image(image, rotation)
# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height - padding

# Move left to right keeping track of the current x position for drawing shapes.
# x = 0

# Alternatively load a TTF font.  Make sure the .ttf font file is in the
# same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)

# Turn on the backlight
backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

x = 0
y = top

print(font.getsize("Ethan"))

# Main loop
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py

    # backlight.value = not (buttonA.value and buttonB.value)

    name = "Ethan's Raspberry Pi"
    cmd = "hostname -I | cut -d' ' -f1"
    IP = "IP: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
    now = datetime.now().strftime("%H:%M:%S")

    x_dist, y_dist = 0, 0
    print("({}, {}) + ({}, {})".format(x,y,x_dist,y_dist), end='\r')
    print()

    # update position
    if not buttonA.value and not buttonA.value:
        x, y = 0, 0
    if not buttonA.value:
        y -= 1
    if not buttonB.value:
        y += 1

    draw.text((x+x_dist, y+y_dist), name, font=font, fill="#FFFFFF")

    # y_dist += font.getsize(name)[1]
    y_dist = 21

    draw.text((x+x_dist,y+y_dist), IP, font=font, fill="#FFFF00")

    # y_dist += font.getsize(IP)[1]
    y_dist = 41

    draw.text((x+x_dist,y+y_dist), now, font=font, fill="#FFFF00")


    # Display image.
    disp.image(image, rotation)
    # time.sleep(0.1)






