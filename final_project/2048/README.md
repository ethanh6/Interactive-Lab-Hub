
# 2048 Game
- Game engine reference: [my past course project](https://github.com/ethanh6/Adversarial_Search_2048_Game)
- Created using pygame

# setup
### setup X forwarding
	- putty config -> connection -> SSH -> X11, enable X!! forwarding
### Set display var
	- export DISPLAY=:<local addr>:0.0
	- my local addr: 172.26.176.1
### enable venv
	```
	$ cd
	$ source circuitpython/bin/activate
	```

# mic and speaker settings
### record audio
	- arecord --format=S16_LE --duration=5 --rate=16000 --file-type=raw out.raw
### play audio
	- aplay --format=S16_LE --rate=16000 out.raw
### adjust volumn 
	- amixer set Master 100%

# to run the game
```python main.py```

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