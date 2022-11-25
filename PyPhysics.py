import math, random, numpy


def addVectors(angle1, length1, angle2, length2):
    """ Returns the sum of two vectors """
    
    x  = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y  = math.cos(angle1) * length1 + math.cos(angle2) * length2
    
    angle  = 0.5 * math.pi - math.atan2(y, x)
    length = math.hypot(x, y)

    return (angle, length)

def collide(p1, p2):

    dx = p1.x - p2.x
    dy = p1.y - p2.y
    
    dist = math.hypot(dx, dy)
    if dist < p1.size + p2.size:
        angle = math.atan2(dy, dx) + 0.5 * math.pi
        total_mass = p1.mass + p2.mass

        (newA, newS) = addVectors(p1.angle, p1.speed*(p1.mass-p2.mass)/total_mass, angle, 2*p2.speed*p2.mass/total_mass)
        (p2.angle, p2.speed) = addVectors(p2.angle, p2.speed*(p2.mass-p1.mass)/total_mass, angle+math.pi, 2*p1.speed*p1.mass/total_mass)
        p1.angle, p1.speed = newA, newS
        elasticity = p1.elasticity * p2.elasticity
        p1.speed *= 0.9
        p2.speed *=0.9

        overlap = 0.5*(p1.size + p2.size - dist+1)
        p1.x += math.sin(angle)*overlap
        p1.y -= math.cos(angle)*overlap
        p2.x -= math.sin(angle)*overlap
        p2.y += math.cos(angle)*overlap

def checkcollisons(ax,ay,bx,by,cx,cy,r):
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    a = pow((bx - ax),2) + pow((by - ay),2)
    b = 2*(ax*(bx - ax) + ay*(by - ay))
    c = pow(ax,2) + pow(ay,2) - pow(r,2)
    disc = pow(b,2) - 4*a*c
    if disc <= 0: return False
    sqrtdisc = math.sqrt(disc)
    t1 = (-b + sqrtdisc)/(2*a)
    t2 = (-b - sqrtdisc)/(2*a)
    if (0 < t1 and t1 < 1) or (0 < t2 and t2 < 1):  return True
    return False
sign = lambda x: math.copysign(1, x)

def distancetocenter(ax,ay,bx,by,cx,cy,slope):
    ax -= cx
    ay -= cy
    bx -= cx
    by -= cy
    if slope!= None: return ay - ax *slope
    return -ax


class Particle:
    """ A circular object with a velocity, size and mass """
    
    def __init__(self, x, y, size, mass=1):
        
        self.x = x
        self.y = y
        self.size = size
        self.colour = (0, 0, 255)
        self.thickness = 0
        self.speed = 0
        self.angle = 0
        self.mass = mass
        self.drag = 1
        self.elasticity = 0.9

    def move(self):
        
        self.x += math.sin(self.angle) * self.speed
        self.y -= math.cos(self.angle) * self.speed
        self.speed *= self.drag

    def accelerate(self, vector):
        self.angle, self.speed = addVectors(self.angle, self.speed, vector[0],vector[1])
        
    def mouseMove(self, mousePos):
        x,y = mousePos
        dx = x - self.x
        dy = y - self.y
        self.angle = 0.5*math.pi + math.atan2(dy, dx)
        self.speed = math.hypot(dx, dy) * 0.1

    def accelerate(self, vA,vL):
        (self.angle, self.speed) = addVectors(self.angle, self.speed, vA, vL)

class Spring:
    def __init__(self, p1, p2, length=50, strength=0.5):
        self.p1 = p1
        self.p2 = p2
        self.length = length
        self.strength = strength
    def update(self):
        dx = self.p1.x - self.p2.x
        dy = self.p1.y - self.p2.y
        dist = math.hypot(dx, dy)
        theta = math.atan2(dy, dx)
        force = (self.length - dist) * self.strength
        self.p1.accelerate(theta + 0.5 * math.pi, force/self.p1.mass)
        self.p2.accelerate(theta - 0.5 * math.pi, force/self.p2.mass)


class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.length = math.sqrt((p2.x - p1.x)**2 + (p2.y-p1.y) **2)
        self.mass = 1000000
        self.angle = math.atan2(self.p2.y - self.p1.y, self.p2.x-self.p1.x)

    def push(self, particle):
        if particle != self.p1 and particle != self.p2:
            self.angle = math.atan2(self.p2.y - self.p1.y, self.p2.x-self.p1.x)
            try: 
                self.slope = (self.p2.y - self.p1.y)/(self.p2.x - self.p1.x)
                self.b = self.p1.y - self.p2.x * self.slope
            except ZeroDivisionError: 
                self.slope = None
                self.b = 0

            if checkcollisons(self.p1.x,self.p1.y,self.p2.x,self.p2.y,particle.x,particle.y,particle.size):
                mod = sign(distancetocenter(self.p1.x,self.p1.y,self.p2.x,self.p2.y,particle.x,particle.y,self.slope))
                while checkcollisons(self.p1.x,self.p1.y,self.p2.x,self.p2.y,particle.x,particle.y,particle.size):
                    direction = self.angle
                    direction = direction  - math.pi/2
                    if mod == -1:
                        if self.slope != 0: particle.x -= 1*math.cos(math.radians(direction)) 
                        if self.slope != None: particle.y -= 1*math.sin(math.radians(direction)) 
                    else: 
                        if self.slope != 0: particle.x += 1*math.cos(math.radians(direction)) 
                        if self.slope != None: particle.y += 1*math.sin(math.radians(direction)) 
                particle.angle = math.pi + ((2 * self.angle)- particle.angle)
                particle.speed *= 0.75

class StaticObject():
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.color = (0, 0, 255)
        self.thickness = 0
        self.mass = 2000000
        self.speed = 1
    def push(self, p1):
        dx = p1.x - self.x
        dy = p1.y - self.y
        
        dist = math.hypot(dx, dy)
        if dist < p1.size + self.size:
            angle = math.atan2(dy, dx) +  0.5 *math.pi
            total_mass = p1.mass + self.mass

            p1.angle, _ = addVectors(p1.angle, p1.speed*(p1.mass-self.mass)/total_mass, angle, 2*self.speed*self.mass/total_mass)
            p1.speed *= 0.9
            overlap = 1*(p1.size + self.size - dist+1)
            p1.x += math.sin(angle)*overlap
            p1.y -= math.cos(angle)*overlap


    

    
class Environment:
    """ Defines the boundary of a simulation and its properties """

    
    def __init__(self, width, height):

        self.gravity = 0
        self.width = width
        self.height = height
        self.particles = []
        self.staticObjects = []
        self.springs = []
        self.edges = []

        self.colour = (255,255,255)
        self.mass_of_air = 0.2
        self.elasticity = 0.75
        self.acceleration = None
        
    def addParticles(self, n=1, **kargs):
        """ Add n particles with properties given by keyword arguments """
    
        for i in range(n):
            size = kargs.get('size', random.randint(10, 20))
            mass = kargs.get('mass', random.randint(100, 10000))
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            particle = Particle(x, y, size, mass)
            particle.speed = kargs.get('speed', random.random())
            particle.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            particle.colour = kargs.get('colour', (0, 0, 255))
            particle.drag = (particle.mass/(particle.mass + self.mass_of_air)) ** particle.size

            self.particles.append(particle)
            return particle

    
    def addSpring(self, p1, p2, length=50, strength=0.5):
        """ Add a spring between particles p1 and p2 """
        self.springs.append(Spring(p1, p2, length, strength))
    
    def addEdge(self, p1, p2):
        self.edges.append(Edge(p1,p2))

    def addStatic(self, x,y, size):
        o = StaticObject(x,y,size)
        self.staticObjects.append(o)
        return o
            

    def update(self):
        """  Moves particles and tests for collisions with the walls and each other """
        
        for i, particle in enumerate(self.particles):
            particle.move()
            (particle.angle, particle.speed) = addVectors(particle.angle, particle.speed, math.pi, self.gravity )
            if self.acceleration:
                particle.accelerate(self.acceleration)
            self.bounce(particle)


            for edge in self.edges:

                edge.push(particle)
            for object in self.staticObjects:
                object.push(particle)
            for particle2 in self.particles[i+1:]:
                collide(particle, particle2)
    
        
        [i.update() for i in self.springs]

    def bounce(self, particle):
        """ Tests whether a particle has hit the boundary of the environment """
        
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
            particle.speed *= self.elasticity

        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle
            particle.speed *= self.elasticity

    def findParticle(self, mousePos):
        """ Returns any particle that occupies position x, y """
        x, y = mousePos
        for particle in self.particles:
            if math.hypot(particle.x - x, particle.y - y) <= particle.size:
                return particle
        return None