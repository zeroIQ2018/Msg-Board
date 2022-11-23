function darkmode(){
    localStorage.setItem('mode', "1");
    a = localStorage.getItem("mode");
}


function lightmode(){
    localStorage.setItem('mode', null);
    a = localStorage.getItem("mode");
}