var last_key;
var pressed_keys = {};
var image_rotated = false;
var getsensorID = setInterval(get_sensor, 1000);

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

function send_keys(json_string){
    if(json_string.length > 2){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "keys.json", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(json_string);
    }
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

function set_size(){
    var myImage = new Image();
    var img = document.getElementById("image");
    myImage.src = img.src;
    var pad = 10;

    var imgW = myImage.width;
    var imgH = myImage.height;
    var bodW = document.body.clientWidth;
    var bodH = document.body.clientHeight;
    var imgR = imgW / imgH;
    var bodR = bodW / bodH;

    var imgDispW = (bodH - 2*pad)*imgR;
    var imgDispH = imgDispW / imgR;
    var panelW = parseInt((bodW-2*pad-imgDispW)/2);
    document.getElementsByClassName("grid-container")[0].setAttribute("style",
    `grid-template-columns: ${panelW}px auto ${panelW}px`);
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

addEvent(window, "resize", set_size);