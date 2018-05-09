var full_data = false;
var text = false;
var tenmins = false;
var thirtymins = false;


window.intervalId = setInterval(function(){
	if (full_data) {
		showGraph(ACCEL_X, 3600);
	} else if (text) {
		showText(ACCEL_X);
	} else if (tenmins) {
	 	showGraph(ACCEL_X, 10);
	} else if (thirtymins) {
	 	showGraph(ACCEL_X, 30);
	} else {
	 	showGraph(ACCEL_X, 15);
	}
}, 10);


showGraph(ACCEL_X, 10);

document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	full_data = true;
	text = false;
	tenmins = false;
	thirtymins = false;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X";
	full_data = false;
	text = true;
	tenmins = false;
	thirtymins = false;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 10 mins";
	full_data = false;
	text = false;
	tenmins = true;
	thirtymins = false;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Acceleration-X: 30 mins";
	full_data = false;
	text = false;
	tenmins = false;
	thirtymins = true;
};


