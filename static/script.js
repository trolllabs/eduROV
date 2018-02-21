var last_key;
var pressed_keys = {};
var image_rotated = false;
var getsensorID = setInterval(get_sensor, 3000);

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

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

function startup() {
}

function send_keys(json_string){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "keys.json", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(json_string);
}

function rotate_image(){
    if (image_rotated){
        image_rotated = false;
        document.getElementById("image").style.transform = "rotate(0deg)";
    } else{
        image_rotated = true;
        document.getElementById("image").style.transform = "rotate(180deg)";
    }
}


function get_sensor(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var left_text = "";
                var sensor = JSON.parse(this.responseText);
                for (var key in sensor) {
                    left_text = left_text.concat(key + ": " + sensor[key] +
                    "<br />");
                }
                document.getElementById("sensordata").innerHTML = left_text;
            }
        };
    xhttp.open("GET", "sensordata.json", true);
    xhttp.send();
}

function resizeToMax(id){
    myImage = new Image()
    var img = document.getElementById(id);
    myImage.src = img.src;
    var imgRatio = myImage.width / myImage.height;
    var bodyRatio = (document.body.clientWidth - 400) / document.body
    .clientHeight;
    if(bodyRatio < imgRatio){
        img.style.width = "100%";
    } else {
        img.style.height = "100%";
    }
}

function setsize(){
    myImage = new Image()
    var img = document.getElementById("image");
    var pad = 10;
    myImage.src = img.src;

    var imgW = myImage.width;
    var imgH = myImage.height;
    var bodW = document.body.clientWidth;
    var bodH = document.body.clientHeight;
    var imgR = imgW / imgH;
    var bodR = bodW / bodH;

    var imgDispW = (bodH - 2*pad)*imgR;
    var imgDispH = imgDispW / imgR;
    var panelW = parseInt((bodW-2*pad-imgDispW)/2);
    console.log(panelW)
    document.getElementById("left-panel").style.width = "${panelW}px";
    document.getElementById("right-panel").style.width = "400px";
}

var addEvent = function(object, type, callback) {
    if (object == null || typeof(object) == 'undefined') return;
    if (object.addEventListener) {
        object.addEventListener(type, callback, false);
    } else if (object.attachEvent) {
        object.attachEvent("on" + type, callback);
    } else {
        object["on"+type] = callback;
    }
}

addEvent(window, "resize", setsize);