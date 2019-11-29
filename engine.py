import pygame, random, math, os, sys
from pygame import gfxdraw as gfx
from pygame.locals import *
import sys

screen = None

def createWindow(width, height):
	win = pygame.display.set_mode((width, height), HWSURFACE | DOUBLEBUF, 32 )
	pygame.display.set_caption("Star Battle")
	pygame.display.flip()
	return win

def initEngine(W, H):
	global screen
	pygame.init()
	screen = createWindow(W,H)

keyDownHandler = None
keyUpHandler = None

def registerKeyEvents(onKeyDown, onKeyUp):
	global keyDownHandler
	global keyUpHandler
	keyDownHandler = onKeyDown
	keyUpHandler = onKeyUp

def runEngine(updateFunc, renderFunc):
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:				
				sys.exit(0)
			if event.type == pygame.KEYUP:
				if keyUpHandler != None:
					keyUpHandler(event.key)
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					sys.exit(0)
				if keyDownHandler != None:
					keyDownHandler(event.key)
					
		screen.fill((0,0,0))
		updateFunc(0.016)
		renderFunc(0.016)
		pygame.display.flip()

def line(x1, y1, x2, y2, color = (255, 255, 255)):
	gfx.line(screen, int(x1), int(y1), int(x2), int(y2), color)

def circle(x, y, r, color = (255, 255, 255)):
	gfx.circle(screen, int(x), int(y), int(r), color)

def drawImg(img, pos, size, angle):
	rot = pygame.transform.rotate(img, angle*180/math.pi)
	screen.blit(img, pos)
	pass