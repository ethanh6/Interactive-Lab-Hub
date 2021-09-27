import time
import subprocess
import digitalio
import board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
import webcolors, os
from adafruit_rgb_display.rgb import color565
from datetime import datetime, timezone, timedelta, date
import pytz

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

class Clock:
    def __init__(self):
        self.state_num = 8
        self.state_ptr = 5
        self.descriptions = \
            ["AM/PM",
            "24 hour",
            "24 hour in binary",
            "Date",
            "Different City",
            "Days left until the end\nof the semester",
            "Bitcoin price",
            "Information"]
    
    def change_mode(self, A, B):

        # display an image
        if A and B:
            print("AB")
        
        elif A:
            self.state_ptr = (self.state_ptr - 1 + self.state_num) % self.state_num
            print("A")
        elif B:
            self.state_ptr = (self.state_ptr + 1) % self.state_num
            print("B")
    
    def get_state(self):
        return self.state_ptr

    def get_info(self):
        time = datetime.now()
        time_str = ""
        if self.state_ptr == 0:
            time_str = time.strftime("%I:%M %p")
        elif self.state_ptr == 1:
            time_str = time.strftime("%H:%M:%S")
        elif self.state_ptr == 2:
            time_tmp = time.strftime("%H:%M:%S")
            hr, min, sec = [str(bin(int(i)))[2:] for i in time_tmp.split(":")]
            time_str = "Hr:  {}\nMin: {}\nSec: {}".format(hr, min, sec)

        elif self.state_ptr == 3:
            time_str = time.strftime("%m/%d/%Y")
            time_str += "\n"

            wd = datetime.today().weekday()
            time_str += ("Monday"    if wd == 0 else
                         "Tuesday"   if wd == 1 else
                         "Wednesday" if wd == 2 else
                         "Thursday"  if wd == 3 else 
                         "Friday"    if wd == 4 else
                         "Saturday"  if wd == 5 else
                         "Sunday"    if wd == 6 else "" )

        elif self.state_ptr == 4:  # timezone
            la_time  = datetime.now(pytz.timezone('US/Pacific')).strftime("%I:%M %p")
            nyc_time = datetime.now(pytz.timezone('US/Eastern')).strftime("%I:%M %p")
            chicago_time = datetime.now(pytz.timezone('America/Chicago')).strftime("%I:%M %p")
            time_str = "New York: {}\nLos Angeles: {}\nChicago: {}".format(nyc_time, la_time, chicago_time)
        
        elif self.state_ptr == 5:
            today = date.today()
            future = date(2021,12,18)
            diff = future - today
            time_str = "\n" + str(diff.days)

        elif self.state_ptr == 6:
            time_str = "$ xxxx"

        elif self.state_ptr == 7:
            name = "Ethan's Raspberry Pi"
            cmd = "hostname -I | cut -d' ' -f1"
            IP = "IP: " + subprocess.check_output(cmd,shell=True).decode("utf-8")
            time_str = "{}\nIP: {}".format(name, IP) 

        return time_str
    
    def get_description(self):
        n = str(self.state_ptr + 1)
        info = n + ". " + self.descriptions[self.state_ptr]
        return info

clock = Clock()

# Main loop
while True:
    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

    #TODO: Lab 2 part D work should be filled in here. You should be able to look in cli_clock.py and stats.py


    # fix position
    x, y = 0, 0

    # update states
    clock.change_mode(not buttonA.value, not buttonB.value)

    description = clock.get_description()
    info = clock.get_info()

    draw.text((x, y), description, font=font, fill="#FFFF00")
    y += font.getsize(description)[1]

    pad = "  \n"
    draw.text((x, y), pad, font=font, fill="#FFFF00")
    y += font.getsize(pad)[1]

    draw.text((x, y), info, font=font, fill="#FFFF00")
    y += font.getsize(info)[1]

    # Display image.
    disp.image(image, rotation)
    time.sleep(0.4)






