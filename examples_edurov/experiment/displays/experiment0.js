function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var total_time = 10;
var elapsed = 0;

sleep(1000)

window.alert("Will now get 30 seconds to try this display");

var x = setInterval(function() {
    if (total_time > elapsed){
        elapsed += 1;
        document.getElementById("timer").innerHTML = total_time-elapsed;
    } else {
        document.getElementById("timer").innerHTML = "EXPIRED";
        window.alert("Click OK to enter the experiment, 1 min");
    }
}, 1000);