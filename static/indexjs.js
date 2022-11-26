function checkEmpty(field){
	if (field == "" ||
		field == null ||
		field == "undefinied"){

		return false;
	}
	else if(/^\s*$/.test(field)){
		return false;
	}
	else{
		return true;
	}
}

document.getElementById("form").onsubmit = function(){

	if((checkEmpty(document.getElementById("messageinput")))){
		alert("Fill the field!");
		return false; 
	}

}


var str = document.getElementById("youtube").src;
var res = str.split("=");
var embeddedUrl = "https://www.youtube.com/embed/"+res[1];
document.getElementById("youtube").src = embeddedUrl;


console.log(localStorage.getItem("mode"));


