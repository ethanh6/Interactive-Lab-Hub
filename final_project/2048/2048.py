from __future__ import print_function
import pygame, sys, time
from pygame import color
from pygame import key
from pygame.locals import *
from random import *

import os, qwiic_joystick, time, sys, webcolors, uuid, json
import paho.mqtt.client as mqtt
import board, busio, adafruit_mpr121
import time, subprocess, digitalio, board
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789
from time import strftime, sleep
from adafruit_rgb_display.rgb import color565

# colours
BLACK = (0, 0, 0)
RED = (244, 67, 54)
PINK = (234, 30, 99)
PURPLE = (156, 39, 176)
DEEP_PURPLE = (103, 58, 183)
BLUE = (33, 150, 243)
TEAL = (0, 150, 136)
L_GREEN = (139, 195, 74)
GREEN = (60, 175, 80)
ORANGE = (255, 152, 0)
DEEP_ORANGE = (255, 87, 34)
BROWN = (121, 85, 72)

colour_dict = { 0:BLACK, 2:RED, 4:PINK, 8:PURPLE, 16:DEEP_PURPLE, 32:BLUE, 64:TEAL, 128:L_GREEN, 256:GREEN, 512:ORANGE, 1024: DEEP_ORANGE, 2048:BROWN}

COLOR = BLUE

def getColour(i):
	return colour_dict[i]

TOTAL_POINTS = 0
DEFAULT_SCORE = 2
BOARD_SIZE = 4

pygame.init()

SURFACE = pygame.display.set_mode((400, 500), 0, 32)
pygame.display.set_caption("2048")

myfont = pygame.font.SysFont("monospace", 25)
scorefont = pygame.font.SysFont("monospace", 50)

tileMatrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
undoMat = []

# joystick
js = qwiic_joystick.QwiicJoystick()

def get_control():
	# joystick
	x, y = js.horizontal, js.vertical
	if (x<200 and (y>300 and y<700)): return True, pygame.K_h
	if (x>800 and (y>300 and y<700)): return True, pygame.K_l
	if (y<200 and (x>300 and x<700)): return True, pygame.K_k
	if (y>800 and (x>300 and x<700)): return True, pygame.K_j

	return False, 98

def main():

	placeRandomTile()
	printMatrix()

	# joystick
	if not js.connected:
		print("Joystick is not connected")
		return
	js.begin()
	print("joystick initialized")

	while True:
		
		# get control signal from circuit
		cond, control = get_control()
		print(cond, control)

		for event in pygame.event.get():
			# quit conditions
			if event.type == QUIT or (event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q)):
				pygame.quit()
				sys.exit()
			# game over condition
			elif (event.type == KEYDOWN and event.key == K_e) or (not checkIfCanGo()):
				printGameOver()
			
			# handle event
			if event.type == KEYDOWN and isArrow_or_HJKL(event.key):

				rotations = getRotations(event.key)

				addToUndo()

				for i in range(0, rotations):
					rotateMatrixClockwise()

				if canMove():
					moveTiles()
					mergeTiles()
					placeRandomTile()

				for j in range(0, (4 - rotations) % 4):
					rotateMatrixClockwise()

				printMatrix()

			if event.type == KEYDOWN:
				global BOARD_SIZE

				if event.key == pygame.K_r:
					reset()

				if 50 < event.key and 56 > event.key:
					BOARD_SIZE = event.key - 48
					reset()

				elif event.key == pygame.K_u:
					undo()

		pygame.display.update()


def printMatrix():

	SURFACE.fill(COLOR)

	global BOARD_SIZE
	global TOTAL_POINTS

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			pygame.draw.rect(SURFACE, getColour(tileMatrix[i][j]), (i*(400/BOARD_SIZE), j*(400/BOARD_SIZE) + 100, 400/BOARD_SIZE, 400/BOARD_SIZE))
			
			label = myfont.render(str(tileMatrix[i][j]), 1, (255,255,255))
			label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255, 255, 255))

			SURFACE.blit(label, (i*(400/BOARD_SIZE) + 30, j*(400/BOARD_SIZE) + 130))
			SURFACE.blit(label2, (10, 20))

def printGameOver():
	global TOTAL_POINTS

	SURFACE.fill(COLOR)

	label = scorefont.render("Game Over!", 1, (255,255,255))
	label2 = scorefont.render("Score:" + str(TOTAL_POINTS), 1, (255,255,255))
	label3 = myfont.render("Press r to restart!", 1, (255,255,255))
	label4 = myfont.render("Press esc or q to quit", 1, (255,255,255))

	SURFACE.blit(label, (50, 100))
	SURFACE.blit(label2, (50, 200))
	SURFACE.blit(label3, (50, 300))
	SURFACE.blit(label4, (50, 400))

def placeRandomTile():
	count = 0
	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE):
			if tileMatrix[i][j] == 0:
				count += 1

	k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	while tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] != 0:
		k = floor(random() * BOARD_SIZE * BOARD_SIZE)

	tileMatrix[floor(k / BOARD_SIZE)][k % BOARD_SIZE] = 2

def floor(n):
	return int(n - (n % 1))

def moveTiles():
	# We want to work column by column shifting up each element in turn.
	for i in range(0, BOARD_SIZE): # Work through our 4 columns.
		for j in range(0, BOARD_SIZE - 1): # Now consider shifting up each element by checking top 3 elements if 0.
			while tileMatrix[i][j] == 0 and sum(tileMatrix[i][j:]) > 0: # If any element is 0 and there is a number to shift we want to shift up elements below.
				for k in range(j, BOARD_SIZE - 1): # Move up elements below.
					tileMatrix[i][k] = tileMatrix[i][k + 1] # Move up each element one.
				tileMatrix[i][BOARD_SIZE - 1] = 0

def mergeTiles():
	global TOTAL_POINTS

	for i in range(0, BOARD_SIZE):
		for k in range(0, BOARD_SIZE - 1):
				if tileMatrix[i][k] == tileMatrix[i][k + 1] and tileMatrix[i][k] != 0:
					tileMatrix[i][k] = tileMatrix[i][k] * 2
					tileMatrix[i][k + 1] = 0
					TOTAL_POINTS += tileMatrix[i][k]
					moveTiles()

def checkIfCanGo():
	for i in range(0, BOARD_SIZE ** 2):
		if tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] == 0:
			return True

	for i in range(0, BOARD_SIZE):
		for j in range(0, BOARD_SIZE - 1):
			if tileMatrix[i][j] == tileMatrix[i][j + 1]:
				return True
			elif tileMatrix[j][i] == tileMatrix[j + 1][i]:
				return True
	return False

def reset():
	global TOTAL_POINTS
	global tileMatrix

	TOTAL_POINTS = 0
	SURFACE.fill(COLOR)

	tileMatrix = [[0 for i in range(0, BOARD_SIZE)] for j in range(0, BOARD_SIZE)]

	main()

def canMove():
	for i in range(0, BOARD_SIZE):
		for j in range(1, BOARD_SIZE):
			if tileMatrix[i][j-1] == 0 and tileMatrix[i][j] > 0:
				return True
			elif (tileMatrix[i][j-1] == tileMatrix[i][j]) and tileMatrix[i][j-1] != 0:
				return True

	return False

def rotateMatrixClockwise():
	for i in range(0, int(BOARD_SIZE/2)):
		for k in range(i, BOARD_SIZE- i - 1):
			temp1 = tileMatrix[i][k]
			temp2 = tileMatrix[BOARD_SIZE - 1 - k][i]
			temp3 = tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k]
			temp4 = tileMatrix[k][BOARD_SIZE - 1 - i]

			tileMatrix[BOARD_SIZE - 1 - k][i] = temp1
			tileMatrix[BOARD_SIZE - 1 - i][BOARD_SIZE - 1 - k] = temp2
			tileMatrix[k][BOARD_SIZE - 1 - i] = temp3
			tileMatrix[i][k] = temp4

def isArrow_or_HJKL(k):
	return(k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT \
	or k == pygame.K_k or k == pygame.K_j or k == pygame.K_h or k == pygame.K_l)

def getRotations(k):
	if k == pygame.K_UP or k == pygame.K_k:
		return 0
	elif k == pygame.K_DOWN or k == pygame.K_j:
		return 2
	elif k == pygame.K_LEFT or k == pygame.K_h:
		return 1
	elif k == pygame.K_RIGHT or k == pygame.K_l:
		return 3
		
def convertToLinearMatrix():
	mat = []

	for i in range(0, BOARD_SIZE ** 2):
		mat.append(tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE])

	mat.append(TOTAL_POINTS)

	return mat

def addToUndo():
	undoMat.append(convertToLinearMatrix())

def undo():
	if len(undoMat) > 0:
		mat = undoMat.pop()

		for i in range(0, BOARD_SIZE ** 2):
			tileMatrix[floor(i / BOARD_SIZE)][i % BOARD_SIZE] = mat[i]

		global TOTAL_POINTS
		TOTAL_POINTS = mat[BOARD_SIZE ** 2]

		printMatrix()


if __name__ == "__main__":
	main()