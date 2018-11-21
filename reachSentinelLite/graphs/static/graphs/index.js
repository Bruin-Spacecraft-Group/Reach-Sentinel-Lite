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
	var numPoints = numPoints;//*60*1000;
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			var temp = new Array();
			var data = new Array();
			for (var i = 0; i < datum.length; i++) {
				datum[i][0] = datum[i][0]/60000;
				temp.push(datum[i][0]);
			}
			var maxTime = Math.max(...temp);
			for (var i = 0; i < datum.length; i++) {
				if (datum[i][0] >= (maxTime - numPoints)) {
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

function showGraph(graphNum, clicked, type){
	var numPoints = 15;
if (clicked){
	var type = type;
	if (type == 1){
		numPoints = 3600;
	} else if (type ==2){
		showText(graphNum);
		return;
	} else if (type ==3){
		numPoints = 10;
	} else if (type ==4){
		numPoints = 30;
	}
	}
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	dataxhttp.send();
	var j = 0;
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			var temp = new Array();
			var data = new Array();
			for (var i = 0; i < datum.length; i++) {
				datum[i][0] = datum[i][0]/60000;
				temp.push(datum[i][0]);
			}
			var maxTime = Math.max(...temp);
			for (var i = 0; i < datum.length; i++) {
				if (datum[i][0] >= (maxTime - numPoints)) {
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
