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

function showGraph(graphNum) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			console.log("Temp data length: " + datum.length);

			var data = new Array();
			for (var i = 0; i < datum.length; i++) {
				datum[i][0] = new Date(datum[i][0])
				data.push(datum[i]);

			}
			drawGraph(data);
		}
	};
}

function showGraph(graphNum, numPoints) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			console.log("Temp data length: " + datum.length);
			var data = new Array();

			if (datum.length <= numPoints) {
				for (var i = 0; i < datum.length; i++) {
					datum[i][0] = new Date(datum[i][0])
					data.push(datum[i]);

				}
			} else {
				for (var i = datum.length-numPoints; i < datum.length; i++) {
					datum[i][0] = new Date(datum[i][0])
					data.push(datum[i]);

				}
			}	
			drawGraph(data);
		}
	};
}


//------------------------
//import Dygraphs;
// should do something upon POST to file

var ACCEL_X = 1;
var ACCEL_Y = 2;
var ACCEL_Z = 3;
var GYRO_X = 4;
var GYRO_Y = 5;
var GYRO_Z = 6;
var BARO = 7;
var TEMP = 8;

var currentSource = document.currentScript.src;






