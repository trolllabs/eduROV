var last_key;
var pressed_keys = {};

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        pressed_keys[evt.keyCode] = 1;
        send_keys(JSON.stringify(pressed_keys))
        last_key = evt.keyCode;
    }
}

document.onkeyup = function(evt) {
    delete pressed_keys[evt.keyCode];
    send_keys(JSON.stringify(pressed_keys))
    last_key = 0;
}

function send_keys(json_string){
    console.log(json_string)
}

function get_sensor(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "sensordata.json", true);
    xhttp.send();
//    document.getElementById("sensordata").innerHTML = 55
}

function resizeToMax(id){
    myImage = new Image()
    var img = document.getElementById(id);
    myImage.src = img.src;
    var imgRatio = myImage.width / myImage.height;
    var bodyRatio = document.body.clientWidth / document.body.clientHeight;
    if(bodyRatio < imgRatio){
        img.style.width = "100%";
    } else {
        img.style.height = "100%";
    }
}
