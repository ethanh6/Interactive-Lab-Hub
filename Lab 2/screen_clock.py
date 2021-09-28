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
import json

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
        self.state_ptr = 0
        self.descriptions = \
            ["AM/PM",
            "24 hour",
            "24 hour in binary",
            "Date",
            "Different City",
            "Days left until the end\nof the semester",
            "Crypto price",
            "Information",
            "Screen Protector"]
    
    def change_mode(self, A, B):

        # display an image
        # prev_ptr = self.state_ptr

        
        if A and (not B):
            self.state_ptr = (self.state_ptr - 1 + self.state_num) % self.state_num
            # print("A")
        elif B and (not A):
            self.state_ptr = (self.state_ptr + 1) % self.state_num
            # print("B")

        # elif A and B:
        #     self.state_ptr = 8
        #     print("AB")
        # else:
        #     self.state_ptr = 0
    
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
        
        elif self.state_ptr == 5:  # days left
            today = date.today()
            future = date(2021,12,18)
            diff = future - today
            time_str = "\n" + str(diff.days)

        elif self.state_ptr == 6:   # bitcoin
            btc_cmd = "curl https://api.coinbase.com/v2/prices/BTC-USD/buy\
             -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' 2> /dev/null"
            btc_data = subprocess.check_output(btc_cmd,shell=True).decode("utf-8")
            btc_price = json.loads(btc_data)['data']['amount']

            eth_cmd = "curl https://api.coinbase.com/v2/prices/ETH-USD/buy\
             -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' 2> /dev/null"
            eth_data = subprocess.check_output(eth_cmd,shell=True).decode("utf-8")
            eth_price = json.loads(eth_data)['data']['amount']

            doge_cmd = "curl https://api.coinbase.com/v2/prices/DOGE-USD/buy\
             -H 'Authorization: Bearer abd90df5f27a7b170cd775abf89d632b350b7c1c9d53e08b340cd9832ce52c2c' 2> /dev/null"
            doge_cmd = subprocess.check_output(doge_cmd,shell=True).decode("utf-8")
            doge_price = json.loads(doge_cmd)['data']['amount']

            time_str = "Bitcoin: {}\nEthereum: {}\nDogecoin: {}".format(str(btc_price), str(eth_price), str(doge_price))

        elif self.state_ptr == 7:   # info page
            name = "Ethan's Raspberry Pi"
            cmd = "hostname -I | cut -d' ' -f1"
            IP = subprocess.check_output(cmd,shell=True).decode("utf-8")
            time_str = "{}\nIP: {}".format(name, IP) 
        
        # show the screen protector
        elif self.state_ptr == 8:
            time_str = "image"

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
    ptr = clock.get_state()
    print(ptr)

    if ptr == 8:
        image = Image.open("red.jpg")

        # Scale the image to the smaller screen dimension
        image_ratio = image.width / image.height
        screen_ratio = width / height
        if screen_ratio < image_ratio:
            scaled_width = image.width * height // image.height
            scaled_height = height
        else:
            scaled_width = width
            scaled_height = image.height * width // image.width
        image = image.resize((scaled_width, scaled_height), Image.BICUBIC)

        # Crop and center the image
        x = scaled_width // 2 - width // 2
        y = scaled_height // 2 - height // 2
        image = image.crop((x, y, x + width, y + height))

    else:
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






