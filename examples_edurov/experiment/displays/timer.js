var training_time = 10;
var experiment_time = 20;
var elapsed = 0;
var server_notified = false;

function stop_car(){
    var length = arrow_key_codes.length;
    for (i = 0; i < length; i++) {
        send_keyup(arrow_key_codes[i]);
    }
}

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

