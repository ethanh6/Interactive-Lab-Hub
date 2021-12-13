
# 2048 Game

# Introduction
This is the classic 2048 game, which is initially developed by Gabriele Cirulli. The objective of the game is to slide and combine the same tiles to reach 2048, but players can continue to play after reaching the goal. 

Originally the player can play only with the arrow keys, now the game has been augmented so that the player can play with multiple control input: joystick, vim-movement, touch sensor, even with their hand with camera!

I implemented the game engine in [my game engine project](https://github.com/ethanh6/Adversarial_Search_2048_Game) using Pygame and OpenCV. Now the player can play the game with different sensors which is connected to the Raspberry Pi server, and since the raspberry pi is connected headlessly, the main game screen will be forwarded to my laptop using X11 forwarding. 

# What you will need
	1. Raspberry Pi
	2. Capacity Sensor
	3. SparkFun Qwiic Joystick
	4. Camera
	5. Banana connector
	6. MiniPi TFT display
	7. Laptop
	8. Internet connection

# Setup X forwarding using Putty and XMing on Windows 11
	1. [download](https://sourceforge.net/projects/xming/) and open XMing as X11 display server.
	2. In Putty
		- make sure the laptop and the Raspberry Pi is under the same network. 
		- configuration -> connection -> SSH -> X11 -> check "enable X11 forwarding"
		- type in the IP of the Raspberry Pi, and start the SSH connection
	3. Clone the project
      	- ```git clone https://github.com/ethanh6/Interactive-Lab-Hub.git```
	4. Connect camera to Raspberry Pi
	5. Streamline the capacity sensor and the joystick
	6. Connect the banana connector to the capacity sensor 0 to 5.

# To run the game
```
$ cd Interactive-Lab-Hub/final_project/2048
$ python main.py
```

# movements in the game
- Arrow keys
- VIM movements (h: LEFT, j: DOWN, k: UP, l: RIGHT)
- controled by joystick
	- push button to undo movement
- controled by gesture 
	- issue: FPS too low
- controled by sound
	- issue: speech to text module not accurate
- controled by capacity sensor
	- 0: up
	- 1: down
	- 2: left
	- 3: right
	- 4: undo
	- 5: end game 

# options in game
- `r` to restart the game.
- `u` to undo a movement.
- `3 ~ 7` to adjust board size (e.g. `3` will change to 3x3 board).
- `e` to jump to game over page.
- `ESC` or `q` to quit the game.
