
# 2048 Game

![machine pic](./imgs/machine.jpg)

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


# Setup X11 forwarding 

1. [download](https://sourceforge.net/projects/xming/) and open XMing as X11 display server.

2. In Putty
	- make sure the laptop and the Raspberry Pi is under the same network. 
	- configuration -> connection -> SSH -> X11 -> check "enable X11 forwarding"
	- type in the IP of the Raspberry Pi, and start the SSH connection

# Setup the physical machine

1. Connect camera to Raspberry Pi

2. Streamline the capacity sensor and the joystick

3. Connect the banana connector to the capacity sensor 0 to 5.


# Setup the project
```
$ pi@ixe00: git clone https://github.com/ethanh6/Interactive-Lab-Hub.git
$ pi@ixe00: virtualenv 2048
$ pi@ixe00: source 2048/bin/activate
$ (2048) pi@ixe00: cd Interactive-Lab-Hub/final_project/2048/
$ (2048) pi@ixe00~/Interactive-Lab-Hub/final_project/2048: pip3 install -r requirements.txt
```

# To run the game
```
$ (2048) pi@ixe00~/Interactive-Lab-Hub/final_project/2048: python main.py
```

> You should be able to see a main game window camera windows pop up.

![screen](./imgs/screen.jpg)
![gameplay](./imgs/game_play.jpg)

# How to play the game

## Rule
Move the tile to merge the same numbers, you win if reach 2048, and you can still play to reach higher score than that.

The game will end if there is no further movements you can perform.

## Keyboard
- Arrow keys
- VIM movements (h: LEFT, j: DOWN, k: UP, l: RIGHT)
- `r` to restart the game.
- `u` to undo a movement.
- `3 ~ 7` to adjust board size, default board size=4 (e.g. `3` will change to 3x3 board).
- `e` to jump to game over page.
- `ESC` or `q` to quit the game.

## Joystick
- Move the joystick to move the tile.
- push button to undo movement

## Gesture 
- Use your finger to point to the direction you want to move the tile (up, down left, right).
- Note: the FPS depends on the internet speed - if the internet connection is slow, then the gesture control might not be as sensitive as expected. 

## Capacity sensor
1. There are 6 options you can do on it, which is labeled on the machine.
2. Connection on the capacity sensor: 
	- 0: up
	- 1: down
	- 2: left
	- 3: right
	- 4: undo
	- 5: end game 

# Application Architecture

![App Architecture](./imgs/archi.jpg)

# Documentation of Design Process

# Demo Video

[Video Link](https://youtu.be/BrQ0-jL41yk)