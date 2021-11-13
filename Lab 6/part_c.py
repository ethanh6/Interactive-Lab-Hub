from __future__ import print_function
import qwiic_joystick
import time
import sys
import paho.mqtt.client as mqtt
import uuid

import board
import busio
import adafruit_mpr121


# stream joystick data and MQTT and 
def main():

	# joy stick setup
	myJoystick = qwiic_joystick.QwiicJoystick()
	if myJoystick.connected == False:
		print("The Qwiic Joystick device isn't connected to the system.", file=sys.stderr)
		return
	myJoystick.begin()
	print("Initialized. Firmware Version: %s" % myJoystick.version)

	# mqtt setup
	client = mqtt.Client(str(uuid.uuid1()))         # Every client needs a random ID
	client.tls_set()                                # configure network encryption etc
	client.username_pw_set('idd', 'device@theFarm') # this is the username and pw we have setup for the class
	client.connect('farlab.infosci.cornell.edu', port=8883) #connect to the broker

	# twizzler sender setup
	i2c = busio.I2C(board.SCL, board.SDA)
	mpr121 = adafruit_mpr121.MPR121(i2c)

	while True:
		cmd = input('>> topic: IDD/')
		if ' ' in cmd:
			print('sorry white space is a no go for topics')
		else:
			topic = f"IDD/{cmd}"
			print(f"now writing to topic {topic}")
			print("type new-topic to swich topics")
			while True:
				val = ""

				# get twizzler msg
				for i in range(12):
					if mpr121[i].value:
						val = "Twizzler {} touched - ".format(i)
					else:
						val = "Twizzler not touched - "


				# get joystick msg
				val += str(("X: %d, Y: %d, Button: %d" % (myJoystick.horizontal,
					myJoystick.vertical, myJoystick.button)))

				if val =='new-topic':
					break
				else:
					client.publish(topic, val)

		time.sleep(.5)



if __name__ == '__main__':
	try:
		main()
	except (KeyboardInterrupt, SystemExit) as exErr:
		print("\nEnding Example 1")
		sys.exit(0)