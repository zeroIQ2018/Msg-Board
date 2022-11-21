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


(function() // to make the thing load on reload
{
  if( window.localStorage )
  {
    if( !localStorage.getItem('firstLoad') )
    {
      localStorage['firstLoad'] = true;
      window.location.reload();
    }  
    else
      localStorage.removeItem('firstLoad');
  }
})();


a = document.getElementById("imgthing").src;


var str = document.getElementById("youtube").src;
var res = str.split("=");
var embeddedUrl = "https://www.youtube.com/embed/"+res[1];
document.getElementById("youtube").src = embeddedUrl;


/*
function ifyoutube(){
	if(a.startsWith("https://www.youtube.com")) 
		{
			console.log("Test");
	document.getElementById("imgthing").type = "iframe";
		}
}

window.onload = ifyoutube();
*/