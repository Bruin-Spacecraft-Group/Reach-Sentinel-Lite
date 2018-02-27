var full_data = false;
var text = false;
var tenmins = false;
var thirtymins = false;

/*
window.intervalId = setInterval(function(){
	if (full_data) {
		showGraph(TEMP, 10);
	} else if (text) {
		showText(TEMP);
	}
	 else if (tenmins) {
	 	showGraph(TEMP, 8);
	 } else if (thirtymins) {
	 	showGraph(TEMP, 7);
	 } else {
	 	showGraph(TEMP, 10);
	 }
}, 10);
*/

showGraph(TEMP, 10);
//showText(TEMP);


document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	full_data = true;
	text = false;
	tenmins = false;
	thirtymins = false;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	full_data = false;
	text = true;
	tenmins = false;
	thirtymins = false;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 10 mins";
	full_data = false;
	text = false;
	tenmins = true;
	thirtymins = false;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 30 mins";
	full_data = false;
	text = false;
	tenmins = false;
	thirtymins = true;
};






