from serial import *
import time
import pygame
from math import pi

#Initialize GPS connection to computer
#ser_gps = serial.Serial("/dev/ttyUSB0", 9600, timeout = 0.01, writeTimeout = 0.01)

def decimal_gps(reference_lon, reference_lat):
    #Convert NMEA format to decimal format
    lon_deg = int(str(reference_lon)[0:2]) #First two digits give degree value
    lat_deg = int(str(reference_lat)[0:2])

    lon_min = float(str(reference_lon)[2:]) #Last digits give minute value
    lat_min = float(str(reference_lat)[2:])
    
    lon_dec = lon_deg + lon_min/60 #Combine degree and minute values for decimal format
    lat_dec = lat_deg + lat_min/60

    return (lon_dec,lat_dec)

def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image

def readgps():
    #Read the GPG LINE using the NMEA standard
    while True:
        line = ser_gps.readline()
        if "GPGGA" in line:
            latitude = line[18:27] #Yes it is positional info for lattitude 3000
            longitude = line[30:40] #do it again 11100

            return(float(longitude), float(latitude))

done = False

# INITIAL PARAMETERS
#Reference NMEA GPS Coordinates
ref_NMEAlon1 = 7917.92002
ref_NMEAlat1 = 4353.68254

ref_NMEAlon2 = 7917.9664
ref_NMEAlat2 = 4353.68014

ref_NMEAlon3 = 7918.0048
ref_NMEAlat3 = 4353.7105

ref_NMEAlon4 = 7918.05154
ref_NMEAlat4 = 4353.70294

#Reference Image Coordinates
ref_x1 = 1079
ref_y1 = 333

ref_x2 = 718
ref_y2 = 355

ref_x3 = 416
ref_y3 = 25

ref_x4 = 52
ref_y4 = 104

#Reference decimal GPS Coordinates
ref_declon1, ref_declat1 = decimal_gps(ref_NMEAlon1,ref_NMEAlat1)
ref_declon2, ref_declat2 = decimal_gps(ref_NMEAlon2,ref_NMEAlat2)
ref_declon3, ref_declat3 = decimal_gps(ref_NMEAlon3,ref_NMEAlat3)
ref_declon4, ref_declat4 = decimal_gps(ref_NMEAlon4,ref_NMEAlat4)

sen1_x = (ref_x2-ref_x1)/(ref_declon2-ref_declon1)
sen1_y = (ref_y2-ref_y1)/(ref_declat2-ref_declat1)

sen2_x = (ref_x3-ref_x1)/(ref_declon3-ref_declon1)
sen2_y = (ref_y3-ref_y1)/(ref_declat3-ref_declat1)

sen3_x = (ref_x4-ref_x1)/(ref_declon4-ref_declon1)
sen3_y = (ref_y4-ref_y1)/(ref_declat4-ref_declat1)

sen4_x = (ref_x3-ref_x2)/(ref_declon3-ref_declon2)
sen4_y = (ref_y3-ref_y2)/(ref_declat3-ref_declat2)

sen5_x = (ref_x4-ref_x2)/(ref_declon4-ref_declon2)
sen5_y = (ref_y4-ref_y2)/(ref_declat4-ref_declat2)

sen6_x = (ref_x4-ref_x3)/(ref_declon4-ref_declon3)
sen6_y = (ref_y4-ref_y3)/(ref_declat4-ref_declat3)

def processAdress(lon,lat):
    (gps_declon,gps_declat) = decimal_gps(lon,lat)

    x1 = ref_x1 + (gps_declon-ref_declon1)*sen1_x
    y1 = ref_y1 + (gps_declat-ref_declat1)*sen1_y

    x2 = ref_x1 + (gps_declon-ref_declon1)*sen2_x
    y2 = ref_y1 + (gps_declat-ref_declat1)*sen2_y

    x3 = ref_x1 + (gps_declon-ref_declon1)*sen3_x
    y3 = ref_y1 + (gps_declat-ref_declat1)*sen3_y

    x4 = ref_x2 + (gps_declon-ref_declon2)*sen4_x
    y4 = ref_y2 + (gps_declat-ref_declat2)*sen4_y

    x5 = ref_x2 + (gps_declon-ref_declon2)*sen5_x
    y5 = ref_y2 + (gps_declat-ref_declat2)*sen5_y

    x6 = ref_x3 + (gps_declon-ref_declon3)*sen6_x
    y6 = ref_y3 + (gps_declat-ref_declat3)*sen6_y

    x = (x1+x2+x3+x4+x5+x6)/6
    y = (y1+y2+y3+y4+y5+y6)/6

    return {'lon':x, "lat":y}

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
size = [1180, 410]
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.display.set_caption("GPS")
myfont = pygame.font.SysFont("monospace", 15)

#Picture of Map
map_img = pygame.image.load('home.PNG')

#Scale map to fit screen
w,h = map_img.get_size()
x_scale = 0.9
y_scale = 0.9
map_img = pygame.transform.scale(map_img, (int(w*x_scale),int(h*y_scale)))

#Arrow represents the GPS location
arrow = pygame.image.load('arrow.png')
arrow = pygame.transform.scale(arrow, (15,15))

#Show the map as long as the user does not close the window
while not done:
	#(lon, lat) = readgps() #Get GPS Coordinates
	lon, lat = 7917.95667, 4353.68

	x = processAdress(lon,lat)['lon'] #Get correponding image coordinates
	y = processAdress(lon,lat)['lat']

	arrowangle = 0
	    
	clock.tick(10)

	for event in pygame.event.get(): # User did something
	    if event.type == pygame.QUIT: # If user clicked close
		done=True # Flag that we are done so we exit this loop

	#pygame.draw.circle(screen, RED, [int(x), int(y)], 10)

	newArrow = rot_center(arrow, arrowangle)
	screen.blit(map_img,(0,0)) #Draw map

	#Reference location drawings
	pygame.draw.circle(screen, RED, [ref_x1, ref_y1], 10)
	pygame.draw.circle(screen, WHITE, [ref_x2, ref_y2], 10)
	pygame.draw.circle(screen, BLUE, [ref_x3, ref_y3], 10)
	pygame.draw.circle(screen, BLACK, [ref_x4, ref_y4], 10)

	#GPS Location drawing
	screen.blit(newArrow,(int(x-7),int(y-4))) #Draw GPS location
	pygame.display.flip()

pygame.quit()
