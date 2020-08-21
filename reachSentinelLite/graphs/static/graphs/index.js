function clearDiv(divName) {
	document.getElementById(divName).innerHTML = "";
	document.getElementById(divName).style.width = "0px";
	document.getElementById(divName).style.width = "0px";
	console.log("\n\n\nIn Clear Div: " + divName + "\n\n\n");
	console.log(document.getElementById(divName).innerHTML);
}

function exchangeSize(one, two) {

	if (two=="textDiv") {
		document.getElementsByClassName(two)[0].innerHTML="";
	} else {
		// reset the inside part of drawChart to what it is before graphs are applied
		document.getElementById(two).innerHTML="";
	}

	// Hardcode for now
	//document.getElementById(one).style.height = document.getElementById(two).style.height;
	//document.getElementById(one).style.width = document.getElementById(two).style.width;

	document.getElementById(one).style.height = "200px";
	document.getElementById(one).style.width = "600px";

	if (two=="textDiv") {
		document.getElementsByClassName(two)[0].style.width = "0px";
		document.getElementsByClassName(two)[0].style.height = "0px";
	} else {
		document.getElementById(two).style.width = "0px";
		document.getElementById(two).style.height = "0px";
	}

}

var curChart;

function drawGraph(dataArray) {
	var lbls = new Array();
	var tgt = new Array();
	for (var i = 0; i < dataArray.length; i++) {
		lbls.push(dataArray[i][0]);
		tgt.push(dataArray[i][1]);
	}

	var ctx = document.getElementById("drawChart").getContext("2d");
	ctx.canvas.height = "300px";
	ctx.canvas.width = "300px";

	var data = {
		labels: lbls,
		datasets: [{
			borderColor: "#c1fdff",
			data: tgt,
			lineTension: 0,
			color: "white"
		}]
	}

	var options = {
		responsive: true,
		tooltips: {
			mode: "index",
			intersect: false
		},
		legend: {
			display: false
		},
		scales: {
			xAxes: [{
				display: true,
				gridLines: {
					display: true,
					color: "#5f5f5f"
				},
				scaleLabel: {
					display: true,
					labelString: "Time elapsed"
				}
			}],
			yAxes: [{
				display: true,
				gridLines: {
					display: true,
					color: "#5f5f5f"
				}
			}]
		},
		animation: {
			duration: 0
		}
	};
	
	if (curChart)
	{
		//curChart.data.labels = lbls;
		//curChart.data.datasets[0].data = tgt;
		curChart.destroy();
		
		Chart.defaults.global.defaultFontColor = "white";
		curChart = new Chart(ctx, {
			type: "line",
			data: data,
			options: options
		});

	}
	else
	{
		Chart.defaults.global.defaultFontColor = "white";
		curChart = new Chart(ctx, {
			type: "line",
			data: data,
			options: options
		});
	}

	//return curChart;

}

function showGraph(graphNum) {
	console.log(arguments.callee.name + " -- 1");
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);  // get the data from the specific graphNum --- how to make this survive legacy?
	dataxhttp.send();
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			console.log("Temp data length: " + datum.length);

			var data = new Array();
			for (var i = 0; i < datum.length; i++) {
				datum[i][0] = new Date(datum[i][0])
				data.push(datum[i]);                                   // performance intensive maybe?

			}
			drawGraph(data);
		}
	};
}

function showGraph(graphNum, clicked, type){
	var numTime = type;

	if (type < 0) {
		switch (type) {
			case -1:
				showText(graphNum);
				return;
		}
	}

	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	//dataxhttp.open("GET", "/graphs/testdata/" + graphNum, true);
	dataxhttp.send();
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];
			var data = new Array();
			var ans = Math.max.apply(Math, datum.map(function(o) {return o[0]}));
			for (var i = 0; i < datum.length; i++) {
				if (datum[i][0] >= (ans - numTime)) {
					datum[i][0] = datum[i][0]/MINS; // EDIT: which format you want x-axis to be? -> curr in mins
					data.push(datum[i]);
				}
			}

			if (document.getElementsByClassName("textDiv")[0].style.width != "0px") {
				exchangeSize("drawChart", "textDiv");
			}

			var mygraph = drawGraph(data);
		}
	};
}

function showText(graphNum) {
	var dataxhttp = new XMLHttpRequest();
	dataxhttp.open("GET", "/graphs/getdata/" + graphNum, true);
	//dataxhttp.open("GET", "/graphs/testdata/" + graphNum, true);
	dataxhttp.send();
	dataxhttp.onreadystatechange = function() {
		if (dataxhttp.readyState == 4 && (dataxhttp.status == 200 || dataxhttp.status == 0)) {
			datum = JSON.parse(dataxhttp.response)['stuff'];

			if (document.getElementById("drawChart").style.width != "0px") {
				exchangeSize("textDiv", "drawChart");
			}
			document.getElementById("textDiv").innerHTML = datum[datum.length-1][1];
		}
	};
}
