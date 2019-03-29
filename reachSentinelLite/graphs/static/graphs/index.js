// following POSIX timestamps -> seconds
const SECS = 1000;
const MINS = 60*SECS;  // 60 seconds
const HOURS = 60*MINS; // 60 minutes

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

// Get ALL the data ---> must give user a warning?
// REDO THIS
function showGraph(graphNum) {
	console.log(arguments.callee.name + " -- 1");
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);  // get the data from the specific graphNum --- how to make this survive legacy?
	dataxhttp.send();
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			console.log("Temp data length: " + datum.length);

			var data = new Array();
			for (var i = 0; i < datum.length; i++) {
				datum[i][0] = new Date(datum[i][0])
				data.push(datum[i]);                                   // performance intensive maybe?

			}
			drawGraph(data);
		}
	};
}

// should we standardize the time units to seconds
// graphNum: desired graph number, find nums at the ____ file
// clicked: whether in initial state or have clicked an option -> default 15 mins timeframe displayed
// type: display type desired -> may need to work a bit more on this
// 			-1: text view
//		 > 0: time in milliseconds

// EXPLORATIONS
// How to have fixed Y-axis?
// For example, for temp, need only between 70-74
// But then, how do we handle outliers? Maybe a blip on the side to note them...
function showGraph(graphNum, clicked, type){
	var numTime = type;

	if (type < 0) {
		switch (type) {
			case -1:
				showText(graphNum);
				return;
		}
	}

	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			var data = new Array();
			var ans = Math.max.apply(Math, datum.map(function(o) {return o[0]}));
			for (var i = 0; i < datum.length; i++) {
				if (datum[i][0] >= (ans - numTime)) {
					datum[i][0] = datum[i][0]/MINS; // EDIT: which format you want x-axis to be? -> curr in mins
					data.push(datum[i]);
				}
			}

			if (document.getElementById("textdiv").style.width != "0px") {
				exchangeSize("graphdiv", "textdiv");
			}
			var graph = drawGraph(data);
		}
	};
}

// ---------- * * * ---------- CHECK HOW TO FORMAT THIS PART; CAN MAKE <P> BUT WILL IT AFFECT GRAPH ELEMS?
// graphNum: desired graph number, find nums at ____ file
function showText(graphNum) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
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
var ALTITUDE;
var BARO = 7;
var TEMP = 8;
