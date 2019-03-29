var clicked = false;
var currFrame = 40*MINS;

window.intervalId = setInterval(showGraph(TEMP, clicked, currFrame), 1000);
//window.intervalId = setInterval(function () { showGraph(TEMP, clicked, currFrame); }, 10);

//showGraph(TEMP, 4);
//showText(TEMP);


document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	clicked = true;
	currFrame = 3600*MINS;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	clicked = true;
	currFrame = -1;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 10 mins";
	clicked = true;
	currFrame = 10*MINS;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 30 mins";
	clicked = true;
	currFrame = 30*MINS;
};
