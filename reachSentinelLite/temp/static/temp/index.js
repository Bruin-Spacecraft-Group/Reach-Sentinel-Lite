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
	dataxhttp.open("GET", "/testGraph/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			datum[1][0] = new Date(datum[1][0]);
			datum[2][0] = new Date(datum[2][0]);

			/*
			for (int i = 0; i < datum.length(); i++) {
				datum[i][0] = new Date(datum[i][0]);
			}
			*/
			drawGraph([datum[1], datum[2]]);

		}
	};
}

//------------------------
//import Dygraphs;

var ACCEL_X = 1;
var ACCEL_Y = 2;
var ACCEL_Z = 3;
var GYRO_X = 4;
var GYRO_Y = 5;
var GYRO_Z = 6;
var BARO = 7;
var TEMP = 8;

var currentSource = document.currentScript.src;

showGraph(TEMP);






