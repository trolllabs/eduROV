//window.alert("Will now get 30 seconds to try this display");
//
//function sleep(ms) {
//  return new Promise(resolve => setTimeout(resolve, ms));
//}

var total_time = 30;
var elapsed = 0;

var x = setInterval(function() {
    if (total_time > elapsed){
        elapsed += 1;
        document.getElementById("timer").innerHTML = total_time-elapsed;
    } else {
        document.getElementById("timer").innerHTML = "EXPIRED";
    }
}, 1000);