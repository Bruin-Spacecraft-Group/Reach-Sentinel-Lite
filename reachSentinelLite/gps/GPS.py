import random
import time
import math
from .velocityFromGps import calcVelGPS

def GPSInit():
  reset = input('Would you like to reset the coordinates? Y/N: ')
  if(str(reset).upper() == 'Y'):
    print('\tReseting coordinates.txt')
    #reset coordinates path
    coor = open('coordinates.txt', 'w+')
    coor.write("")
  print('GPS initiated')

def saveCoor(lon, lat, alt):
  newCoor = ( 
            '%s,%s,%s'
        ) %(lon, lat, alt)

  with open('coordinates.txt', 'a+') as coor: 
        print("lon, lat, alt: " + newCoor)
        coor.write(newCoor + '\n')

  with open("position.kml", "w") as pos:
      kmlHead = (
            """<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://www.opengis.net/kml/2.2">
  <Document>
    <name>Paths</name>
    <description>Examples of paths. Note that the tessellate tag is by default
      set to 0. If you want to create tessellated lines, they must be authored
      (or edited) directly in KML.</description>
    <Style id="yellowLineGreenPoly">
      <LineStyle>
        <color>7f00ffff</color>
        <width>4</width>
      </LineStyle>
      <PolyStyle>
        <color>7f00ff00</color>
      </PolyStyle>
    </Style>
    <Placemark>
      <name>Absolute Extruded</name>
      <description>Transparent green wall with yellow outlines</description>
      <styleUrl>#yellowLineGreenPoly</styleUrl>
      <LineString>
        <extrude>1</extrude>
        <tessellate>1</tessellate>
        <altitudeMode>absolute</altitudeMode>
        <coordinates>\n""" 
            )
      kmlFoot = (
            """</coordinates>
      </LineString>
    </Placemark>
  </Document>
</kml>\n"""
            )
      coor = open('coordinates.txt', 'r')

      pos.write(kmlHead + coor.read() + kmlFoot)

#def processCoordinates(timestamp, longitude, latitude, altitude):
def processCoordinates(longitude, latitude, altitude):

    latDeg = math.floor(latitude)
    lonDeg = math.floor(longitude)

    latMin = latitude - latDeg
    lonMin = longitude - lonDeg
    
    lat = latDeg + latMin/60.0
    lon = lonDeg - lonMin/60.0
    
    saveCoor(lon, lat, altitude)
    '''
    #push the last new value to the old and then set the new value 
    lat1 = lat2
    lat2 = lat
    lon1 = lon2
    lon2 = lon

    #creation of variables for speed calc
    oldTime = newTime
    #update time with timestamp
    newTime = timestamp
    dt = newTime - oldTime
    print("time elapsed: " + str(dt)) 
    calcVelGPS(lat1, lon1, lat2, lon2, dt)
    '''