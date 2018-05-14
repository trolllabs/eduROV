var keycodes = {l:76, c:67, esc:27, enter:13};
var MOTOR_KEYS = [81, 87, 69, 65, 83, 68];
var stat = {light:false, armed:false, roll_ui:true, cinema:false,
            video_rotation:0};
var sensors = {time:0, temp:0, pressure:0, humidity:0, pitch:0, roll:0, yaw:0,
            tempWater:0, pressureWater:0, batteryVoltage:0, free_space:0};
var critical_voltage = 10;
var critical_disk_space = 500;

var sensor_interval = 500;
var interval;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function send_keydown(keycode){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "/keydown="+keycode, true);
    xhttp.setRequestHeader("Content-Type", "text/html");
    xhttp.send(null);
}

function handle_in_browser(keycode){
    if (MOTOR_KEYS.indexOf(keycode) > -1 && !stat.armed){
        if (confirm("The ROV is not armed, do you want to arm it?")) {
            toggle_armed();
        }
        return true;
    } else if (keycode == keycodes.l){
        toggle_light();
        return true;
    } else if (keycode == keycodes.enter){
        toggle_armed();
        return true;
    } else if (keycode == keycodes.esc && stat.cinema){
        toggle_cinema();
        return true;
    } else if (keycode == keycodes.c){
        toggle_cinema();
        return true;
    }
}

function toggle_cinema(){
    stat.cinema = !stat.cinema;
    set_cinema(stat.cinema);
}

function toggle_light(){
    var btn = document.getElementById("lightBtn");
    if(stat.light){
        btn.className = btn.className.replace(" active", "");
    }else{
        btn.className += " active";
    }
    stat.light = !stat.light;
    send_keydown(keycodes.l);
}

function toggle_armed(){
    var btn = document.getElementById("armBtn");
    if(stat.armed){
        btn.className = btn.className.replace(" active", "");
    }else{
        btn.className += " active";
    }
    stat.armed = !stat.armed;
    refresh_ui();
}

function set_update_frequency(){
    var interval = prompt("Set sensor update interval in ms",sensor_interval);
    if (interval){
        if (interval<50){
            alert('Sensor frequency can not be less than 50 ms');
            interval = 50;
        }
        sensor_interval = interval;
    }
}

function toggle_roll(){
    var btn = document.getElementById("rollBtn");
    if(stat.roll_ui){
        document.getElementById("rollOverlay").style.visibility = "hidden";
        btn.className = btn.className.replace(" active", "");
    }else{
        document.getElementById("rollOverlay").style.visibility = "visible";
        btn.className += " active";
    }
    stat.roll_ui = !stat.roll_ui;
}

function stop_rov(){
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "stop", true);
    xhttp.setRequestHeader("Content-Type", "application/text");
    xhttp.send();
}

function rotate_image(){
    stat.video_rotation += 180;
    rotation = stat.video_rotation;
    document.getElementById("image").style.transform =
        `rotate(${rotation}deg)`;
}

function get_sensor(){
    if(stat.armed){
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.stat == 200) {
                var response = JSON.parse(this.responseText);
                for (var key in response) {
                    if (isNaN(response[key])){
                        sensors[key] = response[key];
                    } else{
                        sensors[key] = response[key].toFixed(1)
                    }
                }
                refresh_ui();
            }
        };
        xhttp.open("GET", "sensor.json", true);
        xhttp.send();
    }

    // Reset interval
    interval = setInterval(function () {
        clearInterval(interval);
        get_sensor();
    }, sensor_interval);
}

function refresh_ui(){
    var roll = sensors.roll
    document.getElementById("rollOverlay").style.transform =
        `rotate(${roll}deg)`;

    for (var key in sensors){
        var element = document.getElementById(key);
        if (element){
            if (isNaN(sensors[key])){
                element.innerHTML = sensors[key]
            } else{
                element.innerHTML = sensors[key].toFixed(1);
            }
        }
    }

    // Battery and disk space
    if (sensors.batteryVoltage < critical_voltage){
        document.getElementById("voltageTr").className = "table-danger";
    } else{
        document.getElementById("voltageTr").className.replace("table-danger", "");
    }
    if (sensors.free_space < critical_disk_space){
        document.getElementById("diskTr").className = "table-danger";
    } else{
        document.getElementById("diskTr").className.replace("table-danger", "");
    }
}

get_sensor();