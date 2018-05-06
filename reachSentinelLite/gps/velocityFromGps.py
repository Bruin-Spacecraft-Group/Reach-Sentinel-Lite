import math

def degreesToRadians(degrees):
	return degrees*math.pi / 180

def calcVelGPS (lat1, lon1, lat2, lon2, dt):
	earthRadius = 6371
	dLat = degreesToRadians(lat2 - lat1)
	dLon = degreesToRadians(lon2 - lon1)

	lat1 = degreesToRadians(lat1)
	lat2 = degreesToRadians(lat2)

	a = math.sin(dLat/2)*math.sin(dLat/2) + math.sin(dLon/2)*math.sin(dLon/2)*math.cos(lat1)*math.cos(lat2)
	c = 2*math.atan2(math.sqrt(a), math.sqrt(1-a))

	#dt is in seconds, requires conversion
	#speed is in kph
	speed = earthRadius * c / dt *3600
	print("gps speed: " + str(speed))
	return speed