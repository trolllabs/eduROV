function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var training_time = 10;
var experiment_time = 20;
var training = true;
var elapsed = 0;
var experimenting = false;

sleep(1000)

window.alert("Will now get 30 seconds to try this display.");

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
        if (experiment_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = experiment_time-elapsed;
        } else {
            experimenting = false;
            window.alert("Reposition the robot");
            window.location.replace("/next");
        }
    }
}, 1000);