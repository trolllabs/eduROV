//window.alert("Will now get 30 seconds to try this display");
//
//function sleep(ms) {
//  return new Promise(resolve => setTimeout(resolve, ms));
//}
//
function next_page(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/next124", true);
    xhttp.onload = function() {
                console.log(this.responseURL)
                window.location.replace(this.responseURL);
        };
    xhttp.send();
}
