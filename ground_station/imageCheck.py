import pygame, time

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

# Initialize the game engine
pygame.init()
# Define the colors we will use in RGB format
BLACK = ( 0, 0, 0)
WHITE = (255, 255, 255)
BLUE = ( 0, 0, 255)
GREEN = ( 0, 255, 0)
RED = (255, 0, 0)
ORANGE = (230,255,0)
YELLOW = (125,255,0)
PURPLE = (0,255,255)

# Set the height and width of the screen
size = [1000, 600]
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.display.set_caption("Example code for the draw module")
myfont = pygame.font.SysFont("monospace", 15)

#Picture of Map
map_img = pygame.image.load('UTIAS.PNG')

#Scale map to fit screen
w,h = map_img.get_size()
x_scale = 0.9
y_scale = 0.9
map_img = pygame.transform.scale(map_img, (int(w*x_scale),int(h*y_scale)))

#Arrow represents the GPS location
arrow = pygame.image.load('arrow.png')
arrow = pygame.transform.scale(arrow, (15,15))
arrowangle = 0

x,y = 20,20 #Initial position of arrow
v = 10 #Velocity of arrow

#Show the map as long as the user does not close the window
done = False
while not done:	
	keys = pygame.key.get_pressed()
	if keys[pygame.K_a]:
		x -= v
		if x == -1:
			x = 0
	if keys[pygame.K_d]:
		x += v
		if x == 1501:
			x = 1500
	if keys[pygame.K_w]:
		y -= v
		if y == -1:
			y = 0
	if keys[pygame.K_s]:
		y += v
		if y == 601:
			y = 600
	
	pos = str(x) + " " + str(y)
	label = myfont.render(pos, 1, (0,0,0))
	    
	clock.tick(10)

	for event in pygame.event.get(): # User did something
		if event.type == pygame.QUIT: # If user clicked close
			done=True # Flag that we are done so we exit this loop
		elif event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 1:
				x,y = event.pos

	#pygame.draw.circle(screen, RED, [int(x), int(y)], 10)

	newArrow = rot_center(arrow, arrowangle)
	screen.blit(map_img,(0,0)) #Draw map

	#Reference location drawings
	#pygame.draw.circle(screen, BLUE, [imagex1, imagey1], 10)
	#pygame.draw.circle(screen, WHITE, [imagex2, imagey2], 10)
	#pygame.draw.circle(screen, BLUE, [imagex3, imagey3], 10)
	#pygame.draw.circle(screen, WHITE, [imagex4, imagey4], 10)

	#GPS Location drawing
	screen.blit(newArrow,(int(x-7),int(y-4))) #Draw arrow
	screen.blit(label,(x-30,y-10)) #Draw position
	pygame.display.flip()

pygame.quit()
