var last_key;
var key_dict = {event:'', keycode:0};
var video_rotation = 0;
//var getsensorID = setInterval(get_sensor, 80);
var MINIMUM_PANEL_WIDTH = 250;
var light = false;
var armed = false;
var KEYCODE_L = 76;
var KEYCODE_C = 67;
var rollView = true;
var cinema = false;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

document.onkeydown = function(evt) {
//    if (armed){
        evt = evt || window.event;
        if (evt.keyCode != last_key){
            if (evt.keyCode == KEYCODE_L){
                toggle_light();
            } else if (evt.keyCode == KEYCODE_C){
                toggle_cinema();
            }

            else{
            key_dict['event'] = 'KEYDOWN';
            key_dict['keycode'] = evt.keyCode;
            send_keys(JSON.stringify(key_dict))
            last_key = evt.keyCode;
            }
        }
//    }
//    else{
//        if (confirm("The ROV is not armed, do you want to arm it?")) {
//            toggle_armed();
//        }
//    }
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

function toggle_light(){
    var btn = document.getElementById("lightBtn");
    if(light){
        light = false;
        btn.className = btn.className.replace(" active", "");
    }else{
        light = true;
        btn.className += " active";
    }
    send_keys(JSON.stringify({event:'KEYDOWN', keycode:KEYCODE_L}));
}

function toggle_armed(){
    var btn = document.getElementById("armBtn");
    var command = "";
    if(armed){
        armed = false;
        command = "armed=False"
        btn.className = btn.className.replace(" active", "");
    }else{
        armed = true;
        command = "armed=True"
        btn.className += " active";
    }
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", command, true);
    xhttp.setRequestHeader("Content-Type", "application/text");
    xhttp.send();
}

function stop_rov(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "stop", true);
    xhttp.setRequestHeader("Content-Type", "application/text");
    xhttp.send();
}

function rotate_image(){
    video_rotation += 180;
    document.getElementById("image").style.transform =
        `rotate(${video_rotation}deg)`;
}

function toggle_roll(){
    if(rollView){
        rollView = false;
        document.getElementById("rollOverlay").style.visibility = "hidden";
    }else{
        rollView = true;
        document.getElementById("rollOverlay").style.visibility = "visible";
    }
}

function get_sensor(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var sensor = JSON.parse(this.responseText);
//                sensor['latency'] = calculate_latency().toFixed(1);
                var left_text = "";
                for (var key in sensor) {
                    left_text += "<tr>"
                    left_text += "<td><b>"
                    left_text += key
                    left_text += "</b></td>"
                    left_text += "<td>"
                    if (isNaN(sensor[key])){
                        left_text += sensor[key]
                    } else{
                        left_text += sensor[key].toFixed(1)
                    }
                    left_text += "</td>"
                    left_text += "</tr>"
                }
                var roll = sensor['roll']
                document.getElementById("sensordata").innerHTML = left_text;
                document.getElementById("rollOverlay").style.transform =
                    `rotate(${roll}deg)`;
            }
        };
    xhttp.open("GET", "sensor.json", true);
    xhttp.send();
}

function calculate_latency(){
    var start = Date.now();
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            console.log(Date.now()-Number(this.responseText));
            return Date.now()-Number(this.responseText);
        }
    };
    xhttp.open("GET", "echo="+start.toString(), true);
    xhttp.send();
}

function toggle_cinema(){
    if (cinema){
        cinema = false;
//        window.location.href = "index.html";
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "visible";
        panels[1].style.visibility = "visible";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "relative";
        img.style.width = "100%";
        img.style.marginLeft = "0";
        set_size();
    } else {
        cinema = true;
//        window.location.href = "cinema.html";
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "hidden";
        panels[1].style.visibility = "hidden";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "absolute";
        set_size();
    }
}

function read_file(filename){
    var file = new File(filename);
    file.open("r");
    var str = "";
    while (!file.eof) {
        str += file.readln() + "\n";
    }
    return str
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

    if (cinema){
        var img = document.getElementsByClassName("center-panel")[0];
        var roll = document.getElementsByClassName("rollOverlay")[0];
        if (bodR > imgR){
            var new_width = bodH*imgR;
            var margin = (bodW-new_width)/2;
            img.style.width = new_width.toString();
            img.style.marginLeft = margin.toString();
            roll.style.width = new_width.toString();
        } else {
            var new_width = bodW;
            img.style.width = new_width.toString();
            roll.style.width = new_width.toString();
        }
        var top = new_width/imgR/2*0.9;
        roll.style.top = top.toString();
    }
    else if (bodW<768){
        document.getElementsByClassName("grid-container")[0].setAttribute("style",
        `grid-template-columns: auto`);
    }else{
        var imgDispW = (bodH - 2*pad)*imgR;
        var imgDispH = imgDispW / imgR;
        var panelW = Math.max(parseInt((bodW-2*pad-imgDispW)/2), MINIMUM_PANEL_WIDTH);
        document.getElementsByClassName("grid-container")[0].setAttribute("style",
        `grid-template-columns: ${panelW}px auto ${panelW}px`);

        var realImgW = bodW - 2*panelW - 2*pad;
        var realImhH = realImgW / imgR;

        if (rollView){
            document.getElementsByClassName("rollOverlay")[0].setAttribute("style",
            `width: ${(bodW - 2*panelW - 2*pad)}px;
            top: ${realImhH/2}px`);
        }
    }
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
