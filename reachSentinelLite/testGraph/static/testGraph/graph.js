function csvToArray(csv) {
    return csv.map(function(csv) {
    	return csv.split(",").map(Number);
    });
}

function drawGraph(dataArray) {
	g = new Dygraph(
		document.getElementById("graphdiv"),
		dataArray,
		{}
		);
}

function drawGraphHard(dataArray) {
	g = new Dygraph(
		document.getElementById("graphdiv"),
		"Timestamp,Accel-X, Accel-Y\n" +
					"2017-05-13 16:01:08,0,12\n" +
					"2017-05-13 16:01:09,1,12\n" +
					"2017-05-13 16:01:10,0,13\n" +
					"2017-05-13 16:01:11,0,13\n" +
					"2017-05-13 16:01:12,0,13\n" +
					"2017-05-13 16:01:13,1,12\n" +
					"2017-05-13 16:01:14,0,14\n" +
					"2017-05-13 16:01:15,0,13\n" +
					"2017-05-13 16:01:16,1,12\n" +
					"2017-05-13 16:01:17,0,11\n" +
					"2017-05-13 16:01:18,1,12\n" +
					"2017-05-13 16:01:19,2,13\n" +
					"2017-05-13 16:01:20,1,13\n",
		{}
		);
}

function getData(dataArray, sensor, timestamp) {
	var resultArray = new Array();
	updateTimestamp(timestamp);
	for (i = 0; i < dataArray.length; i++) {
		//resultArray.push(dataArray[i][sensor]);
		resultArray.push([new Date(timestamp), dataArray[i][sensor]]);
		timestamp = updateTimestamp(timestamp);
	}
	return resultArray;
}

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


function showGraph() {
	var filename = "turntable-1.csv";
	var currentSource = document.currentScript.src;
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

			var sensorData = getData(dataArray, ACCEL_Y, timestamp[0]);

			drawGraph(sensorData);
		}
	};
	
	return infoArray;
}

var ACCELX = 0;
var ACCEL_Y = 1;
var ACCEL_Z = 2;
var GYRO_X = 3;
var GYRO_Y = 4;
var GYRO_Z = 5;
var BARO = 6;
var TEMP = 7;

hello = showGraph();