function csvToArray(csv) {
    return csv.map(function(csv) {
    	return csv.split(",").map(Number);
    });
}

function drawGraph(dataArray) {
	g = new Dygraph(
		document.getElementById("graphdiv"),
		dataArray,
		{
			showRoller: true,
			height: 200,
			width: 600
		}
		);
}

function getData(dataArray, sensor, timestamp) {
	var resultArray = new Array();
	for (i = 0; i < dataArray.length; i++) {
		resultArray.push([new Date(timestamp), dataArray[i][sensor]]);
		timestamp = updateTimestamp(timestamp);
	}
	return resultArray;
}

// Hardcoding timestamps into data
function updateTimestamp(timestamp) {
	timestamp = updateSeconds(timestamp);
	if (getSeconds(timestamp) == "00") {
		timestamp = updateMinutes(timestamp);
	}
	if (getSeconds(timestamp) == "00" && getMinutes(timestamp) == "00") {
		timestamp = updateHours(timestamp);
	}
	return timestamp;
}

function getSeconds(timestamp) {
	return timestamp.substring(timestamp.length-2);
}

function updateSeconds(timestamp) {
	seconds = getSeconds(timestamp);
	seconds = parseInt(seconds);
	seconds++;
	if (seconds < 10) {
		return timestamp.substring(0, timestamp.length-2) + "0" + seconds;
	} else if (seconds == 60) {
		return timestamp.substring(0, timestamp.length-2) + "00";
	} else {
		return timestamp.substring(0, timestamp.length-2) + seconds.toString();
	}
}

function getMinutes(timestamp) {
	return timestamp.substring(timestamp.length-5, timestamp.length-3);
}

function updateMinutes(timestamp) {
	minutes = getMinutes(timestamp);
	minutes = parseInt(minutes);
	minutes++;
	if (minutes < 10) {
		return timestamp.substring(0, timestamp.length-5) + "0" + minutes + timestamp.substring(timestamp.length-3);
	} else if (minutes == 60) {
		return timestamp.substring(0, timestamp.length-5) + "00" + timestamp.substring(timestamp.length-3);
	} else {
		return timestamp.substring(0, timestamp.length-5) + minutes.toString() + timestamp.substring(timestamp.length-3);
	}
}

function getHours(timestamp) {
	return timestamp.substring(timestamp.length-8, timestamp.length-6);
}

function updateHours(timestamp) {
	hours = getHours(timestamp);
	hours = parseInt(hours);
	hours++;
	if (hours < 10) {
		return timestamp.substring(0, timestamp.length-8) + "0" + hours + timestamp.substring(timestamp.length-6);
	} else if (hours == 24) {
		return timestamp.substring(0, timestamp.length-8) + "00" + timestamp.substring(timestamp.length-6);
	} else {
		return timestamp.substring(0, timestamp.length-8) + hours.toString() + timestamp.substring(timestamp.length-6);
	}
}
// End time


function showGraph(graphNum) {
	/*
	var filename = "turntable-1.txt";
	var dataSource = currentSource.replace("graph.js", filename);

	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", dataSource, true);
	xhttp.send();
	var infoArray = new Array();
	xhttp.onreadystatechange = function() {
		if (xhttp.readyState == 4 && (xhttp.status == 200 || xhttp.status == 0)) {
			var rawData = xhttp.responseText.split("\n");
			var timestamp = rawData.splice(0, 1);
			var dataArray = csvToArray(rawData);
			var sensorData = getData(dataArray, graphNum, timestamp[0]);
			
			//drawGraph(sensorData);
		}
	};
	*/
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/testGraph/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			console.log(datum[2]);
			datum[1][0] = new Date(datum[1][0]);
			datum[2][0] = new Date(datum[2][0]);
			drawGraph([datum[1], datum[2]]);

		}
	};
}

document.getElementById("ACCEL_X").onclick = function() {
	document.getElementById("hello").innerHTML = "Accel-X over 30 mins:";
	showGraph(ACCEL_X);
};

document.getElementById("ACCEL_Y").onclick = function() {
	document.getElementById("hello").innerHTML = "Accel-Y over 30 mins:";
	showGraph(ACCEL_Y);
};

document.getElementById("ACCEL_Z").onclick = function() {
	document.getElementById("hello").innerHTML = "Accel-Z over 30 mins:";
	showGraph(ACCEL_Z);
};

document.getElementById("GYRO_X").onclick = function() {
	document.getElementById("hello").innerHTML = "Gyro-X over 30 mins:";
	showGraph(GYRO_X);
};

document.getElementById("GYRO_Y").onclick = function() {
	document.getElementById("hello").innerHTML = "Gyro-Y over 30 mins:";
	showGraph(GYRO_Y);
};

document.getElementById("GYRO_Z").onclick = function() {
	document.getElementById("hello").innerHTML = "Gyro-Z over 30 mins:";
	showGraph(GYRO_Z);
};

document.getElementById("BARO").onclick = function() {
	document.getElementById("hello").innerHTML = "Pressure over 30 mins:";
	showGraph(BARO);
};

document.getElementById("TEMP").onclick = function() {
	document.getElementById("hello").innerHTML = "Temperature over 30 mins:";
	showGraph(TEMP);
};

//------------------------

var ACCEL_X = 1;
var ACCEL_Y = 2;
var ACCEL_Z = 3;
var GYRO_X = 4;
var GYRO_Y = 5;
var GYRO_Z = 6;
var BARO = 7;
var TEMP = 8;

var currentSource = document.currentScript.src;

showGraph(ACCEL_X);






