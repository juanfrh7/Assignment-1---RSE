import math
from math import radians, sin, cos, sqrt, atan2

def haversine_distance(lat1, lon1, lat2, lon2):
    """Return the distance in km between two points around the Earth.

    Latitude and longitude for each point are given in degrees.
    """
    lat_dif = radians(lat2-lat1)  #latitude difference
    lon_dif = radians(lon2-lon1)  #longitude difference
    
    #calculate the distance
    a = sin(lat_dif/2) * sin(lat_dif/2) + cos(radians(lat1)) \
        * cos(radians(lat2)) * sin(lon_dif/2) * sin(lon_dif/2)
    
    c = 6371 * 2 * atan2(sqrt(a), sqrt(1-a))

    return c