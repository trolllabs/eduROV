function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var added_delay = 800;

var arrow_key_codes = [38, 40, 39, 37]

var training_time = 10;
var experiment_time = 20;
var training = true;
var elapsed = 0;
var experimenting = false;
var server_notified = false;

var last_key;
var key_dict = {event:'', keycode:0};

document.onkeydown = function(evt) {
    if (experimenting || training){
        await sleep(added_delay);
        evt = evt || window.event;
        if (evt.keyCode != last_key){
            key_dict['event'] = 'KEYDOWN';
            key_dict['keycode'] = evt.keyCode;
            send_keys(JSON.stringify(key_dict))
            last_key = evt.keyCode;
        }
    }
}

document.onkeyup = function(evt) {
    if (experimenting || training){
        await sleep(added_delay);
        key_dict['event'] = 'KEYUP';
        key_dict['keycode'] = evt.keyCode;
        send_keys(JSON.stringify(key_dict))
        last_key = 0;
    }
}

function stop_car(){
    var length = arrow_key_codes.length;
    for (i = 0; i < length; i++) {
        key_dict['event'] = 'KEYUP';
        key_dict['keycode'] = arrow_key_codes[i];
        send_keys(JSON.stringify(key_dict))
    }
}

function send_keys(json_string){
    if(json_string.length > 0){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "/keys.json", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(json_string);
    }
}

await sleep(1000);

window.alert("You will now get 30 seconds to try this display.");

var x = setInterval(function() {
    if (training){
        if (training_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = training_time-elapsed;
        } else {
            stop_car();
            training = false;
            experimenting = true;
            elapsed = 0;
            window.alert("Reposition robot. The real experiment will now last for 60 seconds.");
        }
    }
    else if (experimenting) {
        if (!server_notified){
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/experiment_change?change=start", true);
            xmlHttp.send( null );
            server_notified = true;
        }
        if (experiment_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = experiment_time-elapsed;
        } else {
            stop_car();
            experimenting = false;
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/experiment_change?change=end", true);
            xmlHttp.send( null );
            window.alert("Reposition the robot");
            window.location.replace("/next");
        }
    }
}, 1000);

