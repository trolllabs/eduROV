var training_time = 30;
var experiment_time = 90;
var elapsed = 0;
var server_notified = false;
var base_margin_set = false;

async function stop_car(){
    var length = arrow_key_codes.length;
    for (i = 0; i < length; i++) {
        send_keyup(arrow_key_codes[i]);
    }
    await sleep(added_delay+50);
    for (i = 0; i < length; i++) {
        send_keyup(arrow_key_codes[i]);
    }
}

window.alert("You will now get 30 seconds to try this display.");

var x = setInterval(function() {
    if (exp==1 && !base_margin_set){
                set_base_margin();
                base_margin_set =  true;
    }
    if (training){
        if (training_time > elapsed){
            elapsed += 1;
            document.getElementById("timer").innerHTML = training_time-elapsed;
        } else {
            stop_car();
            training = false;
            experimenting = true;
            elapsed = 0;
            window.alert("Reposition robot. The real experiment will now last for 90 seconds.");
        }
    }
    else if (experimenting) {
        if (!server_notified){
            var xmlHttp = new XMLHttpRequest();
            xmlHttp.open( "GET", "/experiment_change?change=start&exp="+exp,
            true);
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
            xmlHttp.open( "GET", "/experiment_change?change=end&exp="+exp, true);
            xmlHttp.send( null );

            var xhttp = new XMLHttpRequest();
            xhttp.open("GET", "/total_keydowns?amount="+total_n_keydowns+"&exp="+exp,

            true);
            xhttp.setRequestHeader("Content-Type", "text/html");
            xhttp.send(null);

//            window.alert("Reposition the robot");
            window.location.replace("/next");
        }
    }
}, 1000);

