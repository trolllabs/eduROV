function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var training_time = 10;
var experiment_time = 20;
var training = true;
var elapsed = 0;
var experimenting = false;
var server_notified = false;

sleep(1000)

window.alert("You will now get 30 seconds to try this display.");

var x = setInterval(function() {
    if (training){
        if (training_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = training_time-elapsed;
        } else {
            training = false;
            experimenting = true;
            elapsed = 0;
            window.alert("Reposition robot. The real experiment will now last for 60 seconds.");
        }
    }
    else if (experimenting) {
        if (!server_notified){
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/experiment_change?change=start", false);
            xmlHttp.send( null );
            server_notified = true;
        }
        if (experiment_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = experiment_time-elapsed;
        } else {
            experimenting = false;
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/experiment_change?change=end", false);
            xmlHttp.send( null );
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/participant_finished", false);
            xmlHttp.send( null );
            window.alert("Reposition the robot");
            window.location.replace("/next");
        }
    }
}, 1000);