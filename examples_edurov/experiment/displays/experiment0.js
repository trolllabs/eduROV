window.alert("Will now get 30 seconds to try this display");

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function next_page(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "next", true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(json_string);
}

sleep(4000)

next_page()