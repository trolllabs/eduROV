var last_key;
var key_dict = {event:'', keycode:0};

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        last_key = evt.keyCode;
        send_keydown(evt.keyCode);
    }
}

document.onkeyup = async function(evt) {
    last_key = 0;
    send_keyup(evt.keyCode);
}

function send_keydown(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keydown="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

function send_keyup(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keyup="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

function handle_in_browser(keycode){

}