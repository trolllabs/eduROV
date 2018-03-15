var last_key;
var key_dict = {event:'', keycode:0};
var video_rotation = 0;
var getsensorID = setInterval(get_sensor, 80);
var MINIMUM_PANEL_WIDTH = 200;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        key_dict['event'] = 'KEYDOWN';
        key_dict['keycode'] = evt.keyCode;
        send_keys(JSON.stringify(key_dict))
        last_key = evt.keyCode;
    }
}

document.onkeyup = function(evt) {
    key_dict['event'] = 'KEYUP';
    key_dict['keycode'] = evt.keyCode;
    send_keys(JSON.stringify(key_dict))
    last_key = 0;
}

function send_keys(json_string){
    if(json_string.length > 0){
        var xhttp = new XMLHttpRequest();
        xhttp.open("POST", "keys.json", true);
        xhttp.setRequestHeader("Content-Type", "application/json");
        xhttp.send(json_string);
    }
}

function stop_rov(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("POST", "stop", true);
    xhttp.setRequestHeader("Content-Type", "application/text");
    xhttp.send();
}

function rotate_image(){
    video_rotation += 180;
    document.getElementById("image").style.transform =
        `rotate(${video_rotation}deg)`;
}

function get_sensor(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var left_text = "";
                var sensor = JSON.parse(this.responseText);
                for (var key in sensor) {
                    left_text = left_text.concat(key + ": " +
                    sensor[key].toFixed(1) + "<br />");
                }
                var roll = sensor['roll']
                document.getElementById("sensordata").innerHTML = left_text;
                document.getElementById("roll").style.transform =
                    `rotate(${roll}deg)`;
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
    var panelW = Math.max(parseInt((bodW-2*pad-imgDispW)/2), MINIMUM_PANEL_WIDTH);
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
