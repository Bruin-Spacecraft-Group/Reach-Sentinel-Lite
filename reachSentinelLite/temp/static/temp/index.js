/*var full_data = false;
var text = false;
var tenmins = false;
var thirtymins = false;


window.intervalId = setInterval(function(){
	if (full_data) {
		showGraph(TEMP, 1);
	} else if (text) {
		showText(TEMP);
	}
	 else if (tenmins) {
	 	showGraph(TEMP, 10);
	 } else if (thirtymins) {
	 	showGraph(TEMP, 30);
	 } else {
	 	showGraph(TEMP, 15);
	 }
}, 10);
*/
var clicked = false;
var currentType = 0;


window.intervalId = setInterval(showGraph(TEMP, clicked, currentType), 10);

showGraph(TEMP, 4);
//showText(TEMP);


document.getElementById("full_data").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	clicked = true;
	currentType = 1;
};

document.getElementById("text").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature";
	clicked = true;
	currentType = 1;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 10 mins";
	clicked = true;
	currentType = 1;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementById("title").innerHTML = "Temperature: 30 mins";
	clicked = true;
	currentType = 1;
};
