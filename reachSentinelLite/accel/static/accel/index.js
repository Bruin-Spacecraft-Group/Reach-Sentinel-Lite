var clicked = false;
var currFrame = 40*MINS;


window.intervalId = setInterval(showGraph(ACCEL_X, clicked, currFrame), 10);


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
