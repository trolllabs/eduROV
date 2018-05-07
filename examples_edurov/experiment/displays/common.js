function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var added_delay = 500;
var exp = 0;
var arrow_key_codes = [38, 40, 39, 37];
var training = true;
var experimenting = false;
var last_key;
var total_n_keydowns = 0;

function determine_exp(){
    var url = window.location.href;
    if (url.includes("experiment0")){
        exp = 0;
    } else if (url.includes("experiment1")){
        exp = 1;
    } else if (url.includes("experiment2")){
        exp = 2;
    }
}

function update_exp1_keys(keycode, value){
    if (arrow_key_codes.indexOf(keycode) > -1){
        key_status[keycode] = value;
    }
}

document.onkeydown = async function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        last_key = evt.keyCode;
        if (experimenting || training){
            if (exp == 1){
                update_exp1_keys(evt.keyCode, 1);
            }
            if (exp != 2){
                await sleep(added_delay);
            }
            send_keydown(evt.keyCode);
        }
    }
}

document.onkeyup = async function(evt) {
    last_key = 0;
    if (experimenting || training){
        if (exp == 1){
            update_exp1_keys(evt.keyCode, 0);
        }
        if (exp != 2){
            await sleep(added_delay);
        }
        send_keyup(evt.keyCode);
    }
}

function send_keydown(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keydown="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
    total_n_keydowns += 1;
}

function send_keyup(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keyup="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

determine_exp();
