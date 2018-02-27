function clearDiv(divName) {
	document.getElementById(divName).innerHTML = "";
	document.getElementById(divName).style.width = "0px";
	document.getElementById(divName).style.width = "0px";
	console.log("\n\n\nIn Clear Div: " + divName + "\n\n\n");
	console.log(document.getElementById(divName).innerHTML);
}

function exchangeSize(one, two) {

	document.getElementById(two).innerHTML = "";

	// Hardcode for now
	//document.getElementById(one).style.height = document.getElementById(two).style.height;
	//document.getElementById(one).style.width = document.getElementById(two).style.width;

	document.getElementById(one).style.height = "200px";
	document.getElementById(one).style.width = "600px";

	document.getElementById(two).style.width = "0px";
	document.getElementById(two).style.height = "0px";
}

function drawGraph(dataArray) {
	g = new Dygraph(
		document.getElementById("graphdiv"),
		dataArray,
		{
			showRoller: true,
			height: document.getElementById("graphdiv").style.height,
			width: document.getElementById("graphdiv").style.width,
		}
		);
	return g;
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

function showGraph(graphNum, numPoints) { // ---------- * * * ---------- MAKE IT BASED OFF TIME, NOT NUMBER OF DATAPOINTS
	//document.getElementById("dataText").innerHTML = "";
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
					datum[i][0] = new Date(datum[i][0]);
					data.push(datum[i]);
				}
			} else {
				for (var i = datum.length-numPoints; i < datum.length; i++) {
					datum[i][0] = new Date(datum[i][0]);
					data.push(datum[i]);
				}
			}
			if (document.getElementById("textdiv").style.width != "0px") {
				console.log("Text div size is big then\n\n\n\n\n\n\n\n");
				exchangeSize("graphdiv", "textdiv");
			}
			var graph = drawGraph(data);
		}
	};
}

// ---------- * * * ---------- GET DATA BY TIME, NOT DATAPOINTS --- HERE!!!
// ---------- * * * ---------- TIME -> MAJOR FACTOR
/*
function showGraph(graphNum, numMinutes) {
	var timeRange = numMinutes*60*1000;
	var curTime = new Date();
	var curTimeMills = curTime.getTime();
	var startTime = curTimeMills - timeRange;

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
				var objTime = Date(datum[i][0]);
				objTimeMills = objTime.getTime();
				if (objTimeMills >= startTime) {
					datum[i][0] = objTime;
					data.push(datum[i]);
				}
			}
			drawGraph(data);
		}
	};
}
*/
// ---------- * * * ---------- CHECK HOW TO FORMAT THIS PART; CAN MAKE <P> BUT WILL IT AFFECT GRAPH ELEMS?
function showText(graphNum) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];

			if (document.getElementById("graphdiv").style.width != "0px") {
				exchangeSize("textdiv", "graphdiv");
			}
			document.getElementById("textdiv").innerHTML = datum[datum.length-1][1];
		}
	};
}


//------------------------
//import Dygraphs;
// should do something upon POST to file
var TIMESTAMP = 0;
var ACCEL_X = 1;
var ACCEL_Y = 2;
var ACCEL_Z = 3;
var GYRO_X = 4;
var GYRO_Y = 5;
var GYRO_Z = 6;
var MAG_X;
var MAG_Y;
var MAG_Z;
var MAGHEAD;
//var TEMP;
var ALTITUDE;
var BARO = 7;
var TEMP = 8;

var currentSource = document.currentScript.src;






