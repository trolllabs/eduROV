function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

var added_delay = 500;
var exp = 0;
var arrow_key_codes = [38, 40, 39, 37];
var training = true;
var experimenting = false;
var last_key;
var key_dict = {event:'', keycode:0};

function determine_exp(){
    var url = window.location.href;
    if (url.includes("experiment0")){
        exp = 0;
    } else if (url.includes("experiment1")){
        exp = 1;
    }
}

function update_exp1_keys(keycode, value){
    if (arrow_key_codes.indexOf(keycode) > -1){
        key_status[keycode] = value;
    }
}

document.onkeydown = async function(evt) {
    console.log('key DOWN')
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        if (arrow_key_codes.indexOf(evt.keyCode) > -1){
    //        key_dict['event'] = 'KEYDOWN';
    //        key_dict['keycode'] = evt.keyCode;
            last_key = evt.keyCode;
            if (experimenting || training){
                if (exp == 1){
                    update_exp1_keys(evt.keyCode, 1)
                }
                await sleep(added_delay);
    //            send_keys(JSON.stringify(key_dict));
                send_keydown(evt.keyCode);
                console.log('sent DOWN')
            }
        }
    }
}

document.onkeyup = async function(evt) {
    console.log('key UP')
//    key_dict['event'] = 'KEYUP';
//    key_dict['keycode'] = evt.keyCode;
    last_key = 0;
    if (arrow_key_codes.indexOf(evt.keyCode) > -1){
        if (experimenting || training){
            if (exp == 1){
                update_exp1_keys(evt.keyCode, 0)
            }
            await sleep(added_delay);
    //        send_keys(JSON.stringify(key_dict));
            send_keyup(evt.keyCode);
            console.log('sent UP')
        }
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

function send_keydown(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keydown="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

function send_keyup(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keyup="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

determine_exp();
