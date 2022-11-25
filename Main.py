import pygame
import math
import PyPhysics

pygame.display.set_caption('')
width, height = (600, 600)
screen = pygame.display.set_mode((width, height))
env = PyPhysics.Environment(width, height)
env.gravity = 0.02


#Use addParticles to add a simulated particle with parameters 
env.addParticles(x=400, y=250, size=20, speed=1, angle= math.pi/2)
env.addParticles(x=400, y=250, size=8, speed=1, angle= math.pi/2)
plist = []

x= env.addParticles(x=200, y=250, size=5, speed=1, angle= math.pi/2)
y = env.addParticles(x =250, y= 250, size =5, speed = 1, angle = math.pi/2)
x1= env.addParticles(x=200, y=200, size=5, speed=1, angle= math.pi/2)
y1 = env.addParticles(x =250, y= 200, size =5, speed = 1, angle = math.pi/2)

#Use addSpring to add a spring between two particles
env.addSpring(x,y,50,50)
env.addSpring(x1,y,50,50)
env.addSpring(x1,x,50,50)
env.addSpring(y,y1,50,50)
env.addSpring(y1,x1,50,50)
env.addSpring(y1,x,50,50)

#Use this list to create static objects with 0.5 size
slist =[[10,400],[50,400],[50,460], [200,400], [200,440], [400,500]]
for i in slist:
    env.addStatic(i[0], i[1], 2)
elist = [[0,1],[1,2],[3,4],[4,5]]
for i in elist:
    env.addEdge(env.staticObjects[i[0]], env.staticObjects[i[1]])

selected_particle = None
running = True

clock = pygame.time.Clock()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            selected_particle = env.findParticle(pygame.mouse.get_pos())
        elif event.type == pygame.MOUSEBUTTONUP:
            selected_particle = None
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            pass
            #env.addParticles(x = pygame.mouse.get_pos()[0], y =pygame.mouse.get_pos()[1], size = 20)

    if selected_particle:
        selected_particle.mouseMove(pygame.mouse.get_pos())

    env.update()
    screen.fill(env.colour)

    for p in env.particles:
        pygame.draw.circle(screen, p.colour, (int(p.x), int(p.y)) , p.size, p.thickness)
    for s in env.springs:
        pygame.draw.aaline(screen, (0,0,0), (int(s.p1.x), int(s.p1.y)), (int(s.p2.x), int(s.p2.y)))
    for e in env.edges:
        pygame.draw.aaline(screen, (0,0,0), (int(e.p1.x), int(e.p1.y)), (int(e.p2.x), int(e.p2.y)))
    for i in env.staticObjects:
        pygame.draw.circle(screen, i.color, (int(i.x), int(i.y)), i.size )


    pygame.display.flip()
    clock.tick(250)
    #pygame.display.set_caption("FPS: {}".format(round(clock.get_fps())))