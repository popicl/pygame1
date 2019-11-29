from engine import *
import math
import random
from copy import deepcopy
import pygame

def rotate(x,y,angle):
	x1 = x*math.cos(angle) - y*math.sin(angle)
	y1 = x*math.sin(angle) + y*math.cos(angle)
	return x1, y1

W = 1600
H = 900
gravity = 0
nrMeteoriti = int(20*random.random())
nrMeteoriti= 10
#imgMeteor = pygame.image.load("meteor.png")


thrust = 20
aThrust=0.5
blast=100

ship = {
	"type":"ship",
	"x":W/2,
	"y":H/2,
	"vx":0,
	"vy":0,
	"angle":0,
	"dAngle":0,
	"ax":0,
	"ay":0,
	"torque":0,
	"viscosity":0.8,
	"rotViscosity":0.5,
	"r":20,
	"applyThrust":False,
	"fireWeapon":False,
	"fireCooldown":0
}

def getMass(body):
	density = 0.1
	if body["type"] == "glont":
		density = 10
	return density*body["r"]**2
	#return 0.1*body["r"] #less realistic

def createGlont(x,y,vx,vy,lifetime):
	glont = {
		"type":"glont",
		"x":x,
		"y":y,
		"vx":vx,
		"vy":vy,
		"angle":0,
		"dAngle":0,
		"ax":0,
		"ay":0,
		"torque":0,
		"lifetime":lifetime,
		"viscosity":1.0,
		"rotViscosity":0.8,
		"r":5
	}
	return glont

gloante = []

def createMeteor(x,y,vx,vy,r,nrVarfuri,dAngle):
	meteor = {
		"type":"meteor",
		"x":x,
		"y":y,
		"vx":vx,
		"vy":vy,
		"angle":3.14,
		"dAngle":dAngle,
		"ax":0,
		"ay":0,
		"torque":0,
		"viscosity":0.99,
		"rotViscosity":1.0,
		"r":r,
		"nrVarfuri":nrVarfuri,
		"varfuri":[],
		"eSpart": False
	}
	createStea(meteor)
	return meteor

meteoriti = []

def createVarf(x,y):
	varf = {
		"x":x,
		"y":y
	}
	return varf

def createSpring(L,meteor1,meteor2):
	spring = {
		"L":L,
		"m1":meteor1,
		"m2":meteor2
	}
	return spring

springs = []

"""
Tema 1:
	Sa se creeze o lista de meteoriti de diverse raze care se misca cu viteze random pe ecran si fac coliziune cu marginea ecranului
	Meteoritii arata ca nist cercuri maro (255, 128, 0)
	randomath.random() intoarce un numar random intre [0,1)
Tema 2:
	Nava moare cand se ciocneste cu un meteorit si pierzi jocul (se considera ca nava are si ea o forma de cerc sau ca e un punct)
Tema 3:
	Meteoritul moare cand e lovit de un glont.
	Pentru fiecare glont se verifica fiecare meteorit daca este lovit de glont
Tema 4:
	Cand se ciocnesc doi meteoriti intre ei, ricoseaza

Collision intre doua bile:

Varianta 1
Se conserva energia cinetica si impulsul
p1 = m1*v1
p2 = m2*v2
e1 = (m1*v1^2)/2
e2 = (m2*v2^2)/2

(v1,v2) -> ciocnire -> (v1', v2')
Se rezolva sistemul si se obtin v1' si v2'

Varianta 2
Se considera ca bilele sunt de fapt niste campuri de forta elastica. Cand se intrepatrund se resping intre ele cu atat mai tare cu cat distanta dinre ele este mai mica


"""

def getDir(body):
	return math.cos(body["angle"]), math.sin(body["angle"])

def bodiesDist(b1, b2):
	dx = b1["x"]-b2["x"]
	dy = b1["y"]-b2["y"]
	return math.sqrt(dx*dx+dy*dy)

def updatePhysics(body, dt):
	body["x"] += body["vx"]*dt
	body["y"] += body["vy"]*dt

	body["vx"] += body["ax"]*dt
	body["vy"] += body["ay"]*dt

	body["vx"] *= pow(body["viscosity"],dt)
	body["vy"] *= pow(body["viscosity"],dt)

	body["angle"] += body["dAngle"]*dt
	body["dAngle"] += body["torque"]*dt
	
	body["dAngle"] *= pow(body["rotViscosity"], dt)
	collide(body)

def collide(body):
	if body["x"] < 0 and body["vx"] < 0:			#conditia sa nu paraseasca ecranul
		body["vx"] *= -1
	if body["x"] > W and body["vx"] > 0:
		body["vx"] *= -1
	if body["y"] < 0 and body["vy"] < 0:
		body["vy"] *= -1
	if body["y"] > H and body["vy"] > 0:
		body["vy"] *= -1


def applyForce(body, fx, fy):
	# F = m*a
	m = getMass(body)
	body["ax"] += fx / m
	body["ay"] += fy / m
	#print("apply force:",fx,fy,m)

def clearForce(body):
	body["ax"] = 0
	body["ay"] = 0

def clearForces():
	clearForce(ship)
	for g in gloante:
		clearForce(g)
	for m in meteoriti:
		clearForce(m)

def canCollide(a,b):	
	if a["type"] == "glont" and (b["type"] == "ship" or b["type"] == "glont"):
		return False
	if b["type"] == "glont" and (a["type"] == "ship" or a["type"] == "glont"):
		return False
	return True

def breakMeteor (meteor):
	xm=meteor["x"]
	ym=meteor["y"]
	vxm = meteor["vx"]
	vym = meteor["vy"]
	dAnglem=meteor["dAngle"]
	nrVarfurim=meteor["nrVarfuri"]
	rm=meteor["r"]
	meteoriti.remove(meteor)	
	theta = random.random()*math.pi
	dx = math.cos(theta)
	dy = math.sin(theta)
	newVx = 5*(random.random()-0.5)*dx*5
	newVy = 5*(random.random()-0.5)*dy
	newR = rm/2
	if rm/2 > 10:
		m1=createMeteor(xm+dx*newR*1.1, ym+dx*newR, newVx, newVy, newR, nrVarfurim,(random.random()-0.5))
		m1["eSpart"] = True
		meteoriti.append(m1)
		m2=createMeteor(xm-dx*newR*1.1, ym-dx*newR, -newVx, -newVy, newR, nrVarfurim,(random.random()-0.5))
		m2["eSpart"] = True
		meteoriti.append(m2)
		springs.append(createSpring(newR*2.2,m1,m2))
		
		for s in springs:
			if s["m1"] == meteor:
				springs.append(createSpring(bodiesDist(meteor, m1), m1, s["m2"]))
				springs.append(createSpring(bodiesDist(meteor, m2), m2, s["m2"]))
			if s["m2"] == meteor:
				springs.append(createSpring(bodiesDist(meteor, m1), m1, s["m1"]))
				springs.append(createSpring(bodiesDist(meteor, m2), m2, s["m1"]))
		#print (springs)
		
		return m1,m2
		
	
	#return m1,m2

# Collision Effects
def removeGlont(glont):
	if glont in gloante:
		gloante.remove(glont)



def collideBodies(a,b):
	#implosion(a,b)

	if not canCollide(a,b):
		return []
  		
	dx = b["x"] - a["x"]
	dy = b["y"] - a["y"]

	dSquared = dx*dx + dy*dy
	if dSquared >= (b["r"] + a["r"])**2:
		return []

	dist = math.sqrt(dSquared)
	
	if a["type"] == "glont" and b["type"] == "meteor":
		return [
			{ "function": removeGlont, "args":{"glont":a}},
			{ "function": breakMeteor, "args":{"meteor":b}}
		]		
	if b["type"] == "glont" and a["type"] == "meteor" :		
		return [
			{ "function": removeGlont, "args":{"glont":b}},
			{ "function": breakMeteor, "args":{"meteor":a}}
		]		
	

	if dist < 0.000001:
		return []

	dx = b["x"] - a["x"]
	dy = b["y"] - a["y"]
	dSquared = dx*dx + dy*dy
	"""
	if a["type"] == "glont" and b["type"] == "meteor":		#conditia de omorit meteoriti
			gloante.remove(a)
			meteoriti.remove(b)
			return 
	if b["type"] == "glont" and a["type"] == "meteor" :
		gloante.remove(b)
		meteoriti.remove(a)	
		return
	"""
	
	#normalizam vectorul (dx, dy), la final are lungime 1
	dx = dx / dist
	dy = dy / dist

	distFactor = a["r"] + b["r"] - dist
	K = 5000 #constanta de proportionalitate a fortei elastice, cu cat e mai mare cu atat este elasticul mai rigid
	fx = K*dx*distFactor
	fy = K*dy*distFactor
	#applyForce(b, fx, fy)
	#applyForce(a, -fx, -fy)
	return [
		{"function": applyForce, "args":{"body":b, "fx":fx, "fy":fy}},
		{"function": applyForce, "args":{"body":a, "fx":-fx, "fy":-fy}}
	]	

def applyCollisionForces():
	bodies = meteoriti + gloante + [ship]
	effects = []
	#[m0, m1, mN-1, g0, g1,..., ship]
	#bodies[0] e primul meteorit
	for i in range(len(bodies)):
		b1 = bodies[i]
		for j in range(i+1, len(bodies)):
			b2 = bodies[j]
			effects = effects + collideBodies(b1, b2)

	for e in effects:
		function = e["function"]
		args = e["args"]
		#if function != applyForce:
			#print("function:", function)
		function(**args) # call function by unpacking arguments provided as a dictionary in e["args"]

def updateSprings(dt):
	K = 10
	friction = 30
	for s in springs:
		m1 = s["m1"]
		m2 = s["m2"]
		L = s["L"]
		if (not m1 in meteoriti) or (not m2 in meteoriti):
			springs.remove(s)
		else:
			dx = m2["x"] - m1["x"]
			dy = m2["y"] - m1["y"]
			dist = math.sqrt(dx*dx+dy*dy)
			F = K*(dist-L)
			if dist > 0.001:
				dx /= dist
				dy /= dist
				applyForce(m1, F*dx, F*dy)
				applyForce(m2, -F*dx, -F*dy)
				if dist != L:
					# friction force FF = alfa*velocity
					dot1 = dx*m1["vx"]+dy*m1["vy"]
					dot2 = dx*m2["vx"]+dy*m2["vy"]
					vx1 = dot1*dx
					vy1 = dot1*dy
					vx2 = dot2*dx
					vy2 = dot2*dy
					applyForce(m1, -friction*vx1, -friction*vy1)
					applyForce(m2, -friction*vx2, -friction*vy2)




def update(dt):
	clearForces()

	#apply thrust to the ship
	dx, dy = getDir(ship)
	ship["ax"] = dx*ship["applyThrust"]*thrust
	ship["ay"] = dy*ship["applyThrust"]*thrust

	ship["fireCooldown"] -= dt
	if ship["fireWeapon"] and ship["fireCooldown"] <= 0:
		glont = createGlont(ship["x"], ship["y"], dx*blast + ship["vx"], dy*blast + ship["vy"], 10)
		gloante.append(glont)
		ship["fireCooldown"] = 1.1

	updateSprings(dt)

	applyCollisionForces()

	updatePhysics(ship, dt)

	for glont in gloante:
		glont["lifetime"] -= dt
		if glont["lifetime"] > 0:
			updatePhysics(glont, dt)
		else:
			gloante.remove(glont)

	for meteor in meteoriti :
		updatePhysics(meteor,dt)


def drawGlont(glont):
	circle(glont["x"], glont["y"], 5, (255, 255, 0))

def createStea(meteor):
	varfuri=[]
	for i in range(0,meteor["nrVarfuri"]):
		x1= meteor["r"]*math.sin(2*math.pi/meteor["nrVarfuri"]*i)
		y1= meteor["r"]*math.cos(2*math.pi/meteor["nrVarfuri"]*i)
		varfuri.append(createVarf(x1,y1))
		x2= meteor["r"]/2*math.sin(math.pi/meteor["nrVarfuri"]+2*math.pi/meteor["nrVarfuri"]*i)
		y2= meteor["r"]/2*math.cos(math.pi/meteor["nrVarfuri"]+2*math.pi/meteor["nrVarfuri"]*i)
		varfuri.append(createVarf(x2,y2))

	meteor["varfuri"]=varfuri
	#print (meteor)
	return meteor


for i in range (1,nrMeteoriti+1):
	meteor=createMeteor(W*random.random(),H*random.random(),10*(random.random()-0.5),10*(random.random()-0.5),random.randrange(30,100), int(random.randrange(15,26)),random.random()-0.5)
	meteoriti.append(meteor)

def drawMeteor(meteor):
	#drawImg(imgMeteor, (meteor["x"], meteor["y"]), meteor["r"], meteor["angle"])
	#return
	#circle(meteor["x"],meteor["y"],meteor["r"],(255,128,0))

	a=meteor["varfuri"]
	for i in range(0,len(a)):		
		i0=i
		i1=(i+1)%len(a)
		xAr,yAr = rotate(a[i0]["x"] ,a[i0]["y"] ,meteor["angle"])
		xBr,yBr = rotate(a[i1]["x"] ,a[i1]["y"] ,meteor["angle"])

		
		xAr+=meteor["x"]
		yAr+=meteor["y"] 
		xBr+=meteor["x"]
		yBr+=meteor["y"] 
		
		
		line(xAr,yAr,xBr,yBr ,(255,255,255))#(random.randrange(50,200) ,random.randrange(50,200),random.randrange(0,50)))


#for meteor in meteoriti:
#	drawMeteor(meteor)


	


def drawShip(x, y, size, angle):
	xA, yA = 2*size, 0
	xB, yB = -size, size
	xC, yC = -size, -size

	#roate the points
	xA, yA = rotate(xA, yA, angle)	
	xB, yB = rotate(xB, yB, angle)	
	xC, yC = rotate(xC, yC, angle)

	#translate the points with x, y
	xA += x #echivalent cu xA = xA + x
	yA += y
	xB += x
	yB += y
	xC += x
	yC += y

	line(xA, yA, xB, yB)
	line(xB, yB, xC, yC)
	line(xC, yC, xA, yA)

	dx, dy = getDir(ship) # dx, dy is a lenght 1 segment
	L = 10

	#(x0, y0) ---- (x1, y1) segment intre doua puncte
	#un punct (x,y) si o directie (dx,sssssssssssssssssssssssss dy)
	line(xA, yA, xA + dx*L, yA +dy*L)
	circle(x, y, ship["r"], (64, 64, 64))

def render(dt):
	drawShip(ship["x"], ship["y"], ship["r"], ship["angle"])
	for glont in gloante:
		drawGlont(glont)
	for meteor in meteoriti:
		drawMeteor(meteor)
		
	for s in springs:
		line(s["m1"]["x"], s["m1"]["y"], s["m2"]["x"], s["m2"]["y"], (255, 0, 255))
		

   

def onKeyDown(key):
	dx,dy = getDir(ship)
	# apply force in the ship direction or opposite
	if key == pygame.K_w:
		ship["applyThrust"] = 1
	if key == pygame.K_s:
		ship["applyThrust"] = -1
	if key == pygame.K_q:
		pass
	if key == pygame.K_e:
		pass
	if key == pygame.K_SPACE:
		ship["fireWeapon"] = True
		#glont = createGlont(ship["x"], ship["y"], dx*blast + ship["vx"], dy*blast + ship["vy"], 30)
		#gloante.append(glont)

	#rotate the ship with A and D
	if key == pygame.K_a:		
		ship["torque"] = -aThrust
	if key == pygame.K_d:		
		ship["torque"] = aThrust
	

def onKeyUp(key):
	if key == pygame.K_w:
		ship["applyThrust"] = 0		
	if key == pygame.K_s:
		ship["applyThrust"] = 0
	if key == pygame.K_q:
		pass
	if key == pygame.K_e:
		pass

	if key == pygame.K_a:
		ship["torque"] = 0
	if key == pygame.K_d:
		ship["torque"] = 0
	if key == pygame.K_SPACE:
		ship["fireWeapon"] = False
		

initEngine(W, H)
registerKeyEvents(onKeyDown, onKeyUp)
runEngine(update, render)
