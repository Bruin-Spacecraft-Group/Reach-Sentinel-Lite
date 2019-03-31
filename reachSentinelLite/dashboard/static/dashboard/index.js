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

document.getElementById("update").onclick = function() {
	var x = document.getElementsByTagName('iframe');
	for (var i = 0; i < x.length; i++) {
		x[i].contentWindow.location.reload();
	}
	//update(); // EDIT: may be redundant, check and remove
}
