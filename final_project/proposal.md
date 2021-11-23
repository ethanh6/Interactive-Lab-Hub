# Big idea

Build a system where users (players) can play pacman with different interaction. 

### basic features
Player can control the pacman (the main figure) With various input devices such as joystick, capacity sensor and gestures detection (with camera and openCV). I will design a simple program with simple but complete I/O as a game engine, and the player can either play it in a traditional way (with joystick) or with a more intuitive way (with gesture or voice).

### extra features
Besides simply move the pacman around the map, I plan to add features such as switching different themes by certain gestures. Also, another features is that the player can trigger event (such as speed-up or becoming invincible with certain combination of keystroks using the capacity sensor).

# timeline

- 11/22: *Project plan proposal*
- 11/25: finish game engine
- 11/28: simple I/O done - control the game with joystick
- 12/2 : *functional check-off*
- 12/4 : implement openCV gesture recognizer - control with hand
- 12/6 : implement voice recognizer - control with voice
- 12/8 : implement extra features - switch theme with gesture
- 12/13: *final project due*

# parts needed

1. Raspberry pi
2. MiniPi TFT display (output)
3. Joystick (input)
4. Capacity Sensor (input)
5. WebCam camera (intput)
6. WebCam speaker (output)
7. Microphone (input)
8. Extra monitor (output)

# risks/contingencies, and fall-back plans

1. The pacman game engine is difficult to implement
    - fall-back: implement a simpler game such as 2048, with similar I/O logic
2. The openCV software can't recognize the gestures correctly
    - fall-back: instead of trying to construct a simple logic to recognize gestures, using a existing gesture recognizer that can precisely distinguish different hand signs. 
