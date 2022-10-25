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

	if(!(checkEmpty(document.getElementById("usernameinput").value || document.getElementById("messageinput")))){
		alert("Fill the field!");
		return false; 
	}

};