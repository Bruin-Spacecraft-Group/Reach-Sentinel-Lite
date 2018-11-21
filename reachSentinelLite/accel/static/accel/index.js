var clicked = false;
var currentType = 0;


window.intervalId = setInterval(showGraph(ACCEL_X, clicked, currentType), 10);


showGraph(ACCEL_X, 10);

document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	clicked = true;
	currentType = 1;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	clicked = true;
	currentType = 2;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 10 mins";
	clicked = true;
	currentType = 3;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 30 mins";
	clicked = true;
	currentType = 4;
};
