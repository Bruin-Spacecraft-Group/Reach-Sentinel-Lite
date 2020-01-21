var clicked = false;
var currFrame = 4*MINS;

setInterval(function() { myfunc() }, 1000);

function myfunc() {
	showGraph(ACCEL_X, clicked, currFrame);
}

// showGraph(ACCEL_X, 10);

document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	clicked = true;
	currFrame = 3600*MINS;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	clicked = true;
	currFrame = -1;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 10 mins";
	clicked = true;
	currFrame = 10*MINS;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 30 mins";
	clicked = true;
	currFrame = 30*MINS;
};
