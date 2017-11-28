var L = -0.0065 //Temperature lapse rate (K/m)
var M = 0.0289644 //Molar mass of air (kg/mol)
var g = 9.80665 //gravity (m/s^2)
var R = 8.31432 // ideal gas constant (J/mol K)

function altcalc() {
	var initPres = document.getElementById('initialPressure').value
	var temp = document.getElementById('temperature').value
	var pres = document.getElementById('pressure').value
	
    var altitude = ((temp * ((1 / Math.pow((pres / initPres), (R * L)/(g * M))) - 1)) / L)
    console.log(initPres, temp, pres, altitude)
    document.getElementById('result').innerHTML = altitude
}