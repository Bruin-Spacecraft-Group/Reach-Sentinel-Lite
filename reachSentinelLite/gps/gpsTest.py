import random
import time
from velocityFromGps import calcVelGPS

#random values for testing without actual GPS
#should be replaced with parsed GPS coordinates
latDeg = 34
lonDeg = -118
alt = 1000

#reset coordinates path
coor = open('coordinates.txt', 'w+')
coor.write("")
#random increment for stuff
i = -5.0
#garbage values
#these will have no replacement from the data stream
lat2 = 34
lon2 = -118
newTime = time.time()

def printCoor(lon, lat, alt):
  newCoor = ( 
            '%s,%s,%s'
        ) %(lon, lat, alt)

  with open('coordinates.txt', 'a+') as coor: 
        print "lon, lat, alt: " + newCoor
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

while True:
    latMin = 4 + i/10
    lonMin = float(26)
    lat = float(latDeg)+float(latMin)/60
    lon = float(lonDeg)-float(lonMin)/60
    
    printCoor(lon, lat, alt)
    
    #push the last new value to the old and then set the new value 
    lat1 = lat2
    lat2 = lat
    lon1 = lon2
    lon2 = lon

    #creation of variables for speed calc
    oldTime = newTime
    newTime = time.time()
    dt = newTime - oldTime
    print "time elapsed: " + str(dt) 
    calcVelGPS(lat1, lon1, lat2, lon2, dt)
    i += 1
    time.sleep(0.5)
