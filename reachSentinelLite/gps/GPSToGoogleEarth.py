import serial

gps = serial.Serial("/dev/ttyACM0", baudrate = 9600)

while True:
	line = gps.readLine()
	data = line.split(",")
	if data[0] == "$GPRMC":
		if data[2] == "A":

			#convert to decimal degrees
			latGps = float(data[3])
			if data[4] == "S":
				latGps = -latGps
			latDeg = int(latGps/100)
			latMin = latGps - (latDeg*100)
			latitude = latDeg+(latMin/60)

			lonGps = float(data[3])
			if data[4] == "S":
				lonGps = -lonGps
			lonDeg = int(lonGps/100)
			lonMin = lonGps - (lonDeg*100)
			longitude = lonDeg+(lonMin/60)

			print "lat: %s" % latitude
			print "lon: %s" % longitude
			
			#google earth expects the order: longitude, latitude, altitude
			with open ("position.kml", "w") as pos:
				pos.write("""<kml xmlns="http://www.opengis.net/kml/2.2">
  <Placemark>
    <name>Live GPS</name>
    <description>.</description>
    <Point>
      <coordinates>%s,%s,0</coordinates>
    </Point>
  </Placemark>
</kml>""" % (longitude, latitude))

