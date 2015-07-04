import pygame

# INITIAL PARAMETERS
#SCALE FOR MAP
x_factor = 0.8
y_factor = 0.4

#Reference NMEA GPS Coordinates (test location)
ref_NMEAlon1 = 7927.967
ref_NMEAlat1 = 4346.929

ref_NMEAlon2 = 7928.027
ref_NMEAlat2 = 4346.924

ref_NMEAlon3 = 7928.084
ref_NMEAlat3 = 4346.983

ref_NMEAlon4 = 7928.015
ref_NMEAlat4 = 4346.977

#Reference Image Coordinates (test location)
ref_x1 = int(890*x_factor)
ref_y1 = int(489*y_factor)

ref_x2 = int(494*x_factor)
ref_y2 = int(535*y_factor)

ref_x3 = int(128*x_factor)
ref_y3 = int(12*y_factor)

ref_x4 = int(574*x_factor)
ref_y4 = int(70*y_factor)

def decimal_gps(reference_lon, reference_lat):
    #Convert NMEA format to decimal format
    lon_deg = int(str(reference_lon)[0:2]) #First two digits give degree value
    lat_deg = int(str(reference_lat)[0:2])

    lon_min = float(str(reference_lon)[2:]) #Last digits give minute value
    lat_min = float(str(reference_lat)[2:])
    
    lon_dec = lon_deg + lon_min/60 #Combine degree and minute values for decimal format
    lat_dec = lat_deg + lat_min/60

    return (lon_dec,lat_dec)

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
        if "GPGGA" in line and "," not in line[18:27] and "," not in line[30:40]:
            latitude = line[18:27] #Yes it is positional info for lattitude 3000
            longitude = line[30:40] #do it again 11100

            return(float(longitude), float(latitude))
            
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

