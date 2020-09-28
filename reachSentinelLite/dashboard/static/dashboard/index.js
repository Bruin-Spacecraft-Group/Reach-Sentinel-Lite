// seemingly deprecated update functions. now, the graph updates automatically

function update(graphNum) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/updateGraphs/", true);
	//dataxhttp.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
	dataxhttp.send(getCookie('csrftoken'));
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			info = dataxhttp.response;
			document.getElementById("updateText").innerHTML = dataxhttp.response;
		}
	};
}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

/*
document.getElementById("update").onclick = function() {
	var x = document.getElementsByTagName('iframe');
	for (var i = 0; i < x.length; i++) {
		x[i].contentWindow.location.reload();
	}
	//update(); // EDIT: may be redundant, check and remove
}
*/

// added stuff to control the graph. both the accel and temp pages have this, so I figure
// the dashboard needs it too. But since the code is the same between them all, can't we
// move it up into, like, graphs/index.js ? ? ?

var clicked = false;
var currFrame = 40*MINS;

setInterval(function() { myfunc() }, 1000);

function myfunc() {
	showGraph(TEMP, clicked, currFrame);
}

document.getElementById("full_data").onclick = function() {
	document.getElementsByClassName("graphTitle")[0].innerHTML = "Temperature";
	clicked = true;
	currFrame = 3600*MINS;
};

document.getElementById("text").onclick = function() {
	document.getElementsByClassName("graphTitle")[0].innerHTML = "Temperature";
	clicked = true;
	currFrame = -1;
};

document.getElementById("tenmins").onclick = function() {
	document.getElementsByClassName("graphTitle")[0].innerHTML = "Temperature: 10 mins";
	clicked = true;
	currFrame = 10*MINS;
};

document.getElementById("thirtymins").onclick = function() {
	document.getElementsByClassName("graphTitle")[0].innerHTML = "Temperature: 30 mins";
	clicked = true;
	currFrame = 30*MINS;
};
