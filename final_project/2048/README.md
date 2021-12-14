
# 2048 Game

# Introduction

![header](./imgs/header.jpg)

This is the classic 2048 game, which is initially developed by Gabriele Cirulli. The objective of the game is to slide and combine the same tiles to reach 2048, but players can continue to play after reaching the goal. 

Originally the player can play only with the arrow keys, now the game has been augmented so that the player can play with multiple control input: joystick, vim-movement, touch sensor, even with their hand with camera!

I implemented the game engine in [my game engine project](https://github.com/ethanh6/Adversarial_Search_2048_Game) using Pygame and OpenCV. Now the player can play the game with different sensors which is connected to the Raspberry Pi server, and since the raspberry pi is connected headlessly, the main game screen will be forwarded to my laptop using X11 forwarding. 

![machine pic](./imgs/machine.jpg)

# What you will need

1. Raspberry Pi

2. Capacity Sensor

3. SparkFun Qwiic Joystick

4. Webcam

5. Banana connector

6. MiniPi TFT display

7. Laptop

8. Internet connection


# Setup X11 forwarding on Windows 11

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

> You should be able to see a main game window and a camera window pop up.

![screen](./imgs/screen.jpg)
![gameplay](./imgs/game_play.jpg)

# How to play the game

## Rule
Move the tile to merge the same numbers, you win if reach 2048. 

You can still play to achieve higher score than 2048.

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

![js](./imgs/joystick.jpg)

## Gesture 
- Use your finger to point to the direction you want to move the tile (up, down left, right).
- Note: the FPS depends on the internet speed - if the internet connection is slow, then the gesture control might not be as sensitive as expected. 

![gesture](./imgs/gesture.jpg)

> As you can see in the picture, the camera detects the "right" gesture, and the movement log in the terminal correctly show that this is gesture to the direction "right".

## Capacity sensor
1. There are 6 options you can do on it, which is labeled on the machine.
2. Connection on the capacity sensor: 
	- 0: up
	- 1: down
	- 2: left
	- 3: right
	- 4: undo
	- 5: end game 

![cap sensor](./imgs/capsensor.jpg)
![cap sensor inside](./imgs/cap_inside.jpg)

# Application Architecture

![App Architecture](./imgs/archi.jpg)

# State Diagram

![State Diagram](./imgs/state.jpg)

# Documentation

## Timeline

- 11/22: *Project plan proposal*
- 11/24: *project feedback*
- 11/25: finish game engine
- 11/28: simple I/O done - control the game with joystick and capacity sensor
- 12/2 : *functional check-off*
- 12/4 : implement openCV gesture recognizer - control with hand
- 12/10 : implement extra features - switch theme with gesture
- 12/7 : *project demo*
- 12/8 : tried implement voice recognizer - control with voice
- 12/13: *final project writeup due*

## Structure of the repo
```
Interactive-Lab-Hub
└───Lab 1
└───Lab 2
└───Lab 3
└───Lab 4
└───Lab 5
└───Lab 6
└───final_project
|   |   proposal.md                   -> project proposal
│   └───Pacman                        -> (archive of pacman)
│   └───2048                          -> main project directory
│       |   main.py                   -> main game engine
│       |   README.md                 -> this READ.md
│       |   HandTrackingModule.py     -> gesture detection module
│       |   requirements.txt          -> package requirements
│       └───imgs                      -> images for the readme
│       └───speech                    -> (archive for speech module)
```

## Design Process

This project is inspired by the project demo at the start of the semester, where a previous student's project enables player to play Flappy-Bird with their head movements. The main idea of this project is to design a similar control input on different game. 

Initially, I wanted to design a Pacman game with various control inputs. However, when I tried to implement the game, I realized that there was a technical difficulty - Pacman heavily relies on real-time movements which are required to be detected instantly. That is not feasible while using the OpenCV on raspberry pi, which possesses limited computational power. 

Instead, I turned to another game that does not require instant movement detection - 2048, with the same inputs that are used to be in Pacman. 

As for the game engine, I re-used the 2048 game that I implemented in a previous course written in Pygame, with augmentations that accept extra input such as joystick and capacity sensor. It took me about 3 days to finalized the main game engine setup, with joystick and capacity sensor successfully installed. Also I added Vim-movements since I'm a vim lover.

The first obstable that I encourtered is how to foward the raspberry pi display, from Pygame, to my laptop using SSH. Initially, I connected a monitor to the Pi to develop the game, but obviously, headless mode would be the optimal way to demostrate the project as well as to develop on my laptop. It actually took me two days to finalized the X11 forwarding settings since I was not familiar with this technologies. This is the main reason why the machine did not work in the day of project demo, but the problem has been fixed now.

When I implemented the gesture detection feature, I realized that the low FPS would be problematic and affect the player's experience. To optimize the gesture detection module that we used in previous lab, I removed redundant parts and only kept the index finger and thumb since those are all it requires to detect a direction. This optimization method significantly improved the FPS from 0.1 to 2, however, it still depends on the speed of the internet connection.

The next problem I faced is to implement voice control feature. In the ideal situation, the player can say, for example, "right" or "up". to move the tile. However, the Vosk module did not work as expected - it's able to detect numbers, but it doesn't recognize words like "left" and "down". It took me another two days to try implementing this feature, but I eventually removed it not only because the accuracy issue, but also the concern that combining voice recognition and gesture detection might even drain the performance of Pi. 

There is also a problem that slightly lower the player's experience - it took about 7 seconds for the program to start. I believed it is due to the performance of the Raspberry Pi.

## Change of Design

1. Game engine: Pacman -> 2048
2. Remove voice input


## Next Step

1. Minimize the OpenCV module to improve FPS
2. Optimize voice control
3. Add other sensor such as approximity sensor or GyroScope sensor.
4. Add different modes, such as Gesture mode or Keyboard mode, where a player only play with single inputs. This might improve the low FPS issue.
5. Improve 2048 animation.


## Reflection and Conclusion

> What have you learned or wish you knew at the start of the project?

This is an interesting project to work on, and it is always intriguing to experiment with different inputs. The main functionality such as joystick, keyboard input and capacity sensor are easier to implement than voice control and gesture detection, however, the latter part is more interesting. 

I spent tremendous amount of time working on the game engine, and I believe that this project does help me better understand the pygame module. 

To implement a game with various control, I think the crutial thing to recognize is to find the best control input with the right machine. For example, the joystick and keyboard work the best in terms of reaction time and user experience. 

Besides the interaction part, I have learnt a lot other knowledges such as SSH with X11 fowrarding, OpenCV and Pygame design throughout the project.


# Team

Ethan Huang (eh543)


# Demo Video

[Video Link](https://youtu.be/BrQ0-jL41yk)

Player credit: Kristjan Tomasson

> Hope you enjoy the project and thank you for this semester!