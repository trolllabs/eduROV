function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var training_time = 10;
var experiment_time = 20;
var training = true;
var elapsed = 0;

sleep(1000)

window.alert("Will now get 30 seconds to try this display.");

var x = setInterval(function() {
    if (training){
        if (training_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = training_time-elapsed;
        } else {
            window.alert("Reposition robot. The real experiment will now last for 60seconds.");
            training = false;
            elapsed = 0;
        }
    else {
        if (experiment_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = experiment_time-elapsed;
        } else {
            window.alert("Done!");
        }
    }
}, 1000);