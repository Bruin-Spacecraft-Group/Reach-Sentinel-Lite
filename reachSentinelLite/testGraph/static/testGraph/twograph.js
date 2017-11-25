$.ajax({
    type: "GET",
    url: '/getdata/',
    success: function(response){
    	document.getElementById("testing").innerHTML = "This is some text";
    },
    error: function(jqXHR, textStatus, errorThrown){
        // handle any errors here
        // Call models here.
    }
});