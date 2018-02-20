var last_key;
var pressed_keys = {};
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
    console.log(json_string)
}


function get_sensor(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var left_text = "";
                var sensor = JSON.parse(this.responseText);
                for (var key in sensor) {
                    left_text = left_text.concat(key + ": " sensor[key] +
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
