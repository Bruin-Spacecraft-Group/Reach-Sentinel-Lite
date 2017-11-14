function testFunction(data, dataArray, source) {
	console.log(source);
	var xhttp = new XMLHttpRequest();
	xhttp.open("GET", source, true);
	xhttp.onreadystatechange = function(dataArray) {
		if (this.readyState == 4 && this.status == 200) {
			console.log("Value of Data:\t" + data.valueOf());
			var info = this.responseText;
			dataArray = info.split("\n");
			console.log("Value of Data Array:\t" + dataArray[1]);
			document.getElementById("tester").innerHTML = this.responseText;
		}
	};
	var info = xhttp.responseText;
	dataArray = info.split("\n");
	xhttp.send();
	
}


//import Dygraph from 'dygraphs';
var filename = "turntable-1.txt";
var currentSource = document.currentScript.src;
var dataSource = currentSource.replace("graph.js", filename);


var data = "testing out here";
var dataArray = [];

console.log(dataSource);
testFunction(data, dataArray, dataSource);
console.log("Data Array Outside-0:\t" + dataArray.length);
console.log("---------------------------------------------");

console.log("Data outside the function:\t" + data);
var allData = data.split("\n");
console.log("Type of allData:\t" + typeof(allData));
console.log("First value of allData:\t" + allData[1]);
for (i = 0; i < allData.length; i++) {
	console.log(allData[i]);
}












g = new Dygraph(
	document.getElementById("graphdiv"),

	"Timestamp,Accel-X, Accel-Y\n" +
	"2017-05-13 16:01:08,0,12\n" +
	"2017-05-13 16:01:09,1,12\n" +
	"2017-05-13 16:01:10,0,13\n" +
	"2017-05-13 16:01:11,0,13\n" +
	"2017-05-13 16:01:12,0,13\n" +
	"2017-05-13 16:01:13,1,12\n" +
	"2017-05-13 16:01:14,0,14\n" +
	"2017-05-13 16:01:15,0,13\n" +
	"2017-05-13 16:01:16,1,12\n" +
	"2017-05-13 16:01:17,0,11\n" +
	"2017-05-13 16:01:18,1,12\n" +
	"2017-05-13 16:01:19,2,13\n" +
	"2017-05-13 16:01:20,1,13\n",
	{}
	);


/*

	"Date,Temperature\n" +
    "2009/07/12 12:34:56,75\n" +
    "2009/07/12 12:34:57,70\n" +
    "2009/07/12 12:34:58,90\n" +
    "2009/07/12 12:34:59,85\n" +
    "2009/07/12 12:35:00,87\n",
*/



/*
xhttp.open("GET", info, true);
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
		console.log("Value of Data:\t" + data.valueOf());
		data = this.responseText;
		console.log("Value of Data2:\t" + data);
		document.getElementById("tester").innerHTML = this.responseText;
	}
};
xhttp.send();
*/