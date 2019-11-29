from engine import *


W = 1600
H = 900
gravity = 10

def update(dt):
	global shipX, shipY
	global vx, vy
	shipX=shipX+vx*dt
	shipY=shipY+vy*dt
	vx=vx+ax*dt
	vy=vy+(ay+gravity)*dt
	vx=vx*pow(0.9,dt)
	vy=vy*pow(0.9,dt)

	if shipX < 0 and vx < 0:
		vx=-vx
	if shipX > W and vx > 0:
		vx=-vx
	if shipY < 0 and vy < 0:
		vy= -vy
	if shipY >  H and vy > 0:
		vy=-vy
	

shipX = W/2
shipY = H/2
shipSpeed = 100
thrust = 100
vx=0
vy=0
ax=0
ay=0

def drawShip(x,y,size):
	line(x,y-size,x-size,y+size)
	line(x-size,y+size,x+size,y+size)
	line(x+size,y+size,x,y-size)

def render(dt):
	drawShip(shipX, shipY, 30)

def onKeyDown(key):
	global ax, ay
	if key == pygame.K_w:
		ay=-thrust
	if key == pygame.K_a:
		ax=-thrust
	if key == pygame.K_s:
		ay=thrust
	if key == pygame.K_d:
		ax=thrust
	

def onKeyUp(key):
	global ax, ay
	if key == pygame.K_w:
		ay=0
	if key == pygame.K_a:
		ax=0
	if key == pygame.K_s:
		ay=0
	if key == pygame.K_d:
		ax=0


initEngine(W, H)
registerKeyEvents(onKeyDown, onKeyUp)
runEngine(update, render)
