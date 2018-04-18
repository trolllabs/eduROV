var last_key;
var key_dict = {event:'', keycode:0};

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        key_dict['event'] = 'KEYDOWN';
        key_dict['keycode'] = evt.keyCode;
        send_keys(JSON.stringify(key_dict))
        last_key = evt.keyCode;
    }
}

document.onkeyup = function(evt) {
    key_dict['event'] = 'KEYUP';
    key_dict['keycode'] = evt.keyCode;
    send_keys(JSON.stringify(key_dict))
    last_key = 0;
}

function send_keys(json_string){
    if(json_string.length > 0){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "keys.json", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(json_string);
    }
}
