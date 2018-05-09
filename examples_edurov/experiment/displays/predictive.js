var up = 38;
var down = 40;
var right = 39;
var left = 37;
var key_status = {up: 0, down: 0, right: 0, left:0};
var base_margin = 0;
var base_image_width = 1024;
var pixel_turn_rate = 30;
var pixel_scale_rate = 5;

var horizontal_move = 0;
var scale_move = 0;
var horizontal_px_move = 0;
var scale_px_move = 0;

var update_interval = 25;
var perceived_delay = 710;


var bodW = 0;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function update_hor_with_delay(amount, delay){
    await sleep(delay);
    horizontal_move += amount;
}

async function update_scale_with_delay(amount, delay){
    await sleep(delay);
    scale_move += amount;
}

var x = setInterval(function() {
    if (key_status[up]){
        scale_move += 1;
        update_scale_with_delay(-1, perceived_delay);

        var factor = 0.8;
        if (key_status[left]){
            horizontal_move += factor;
            update_hor_with_delay(-factor, perceived_delay);
        } else if (key_status[right]){
            horizontal_move -= factor;
            update_hor_with_delay(+factor, perceived_delay);
        }
    } else if (key_status[down]){
        scale_move -= 1;
        update_scale_with_delay(1, perceived_delay);

        var factor = -0.8;
        if (key_status[left]){
            horizontal_move += factor;
            update_hor_with_delay(-factor, perceived_delay);
        } else if (key_status[right]){
            horizontal_move -= factor;
            update_hor_with_delay(+factor, perceived_delay);
        }
    } else if (key_status[left]){
        horizontal_move += 1;
        update_hor_with_delay(-1, perceived_delay);
    } else if (key_status[right]){
        horizontal_move -= 1;
        update_hor_with_delay(+1, perceived_delay);
    }

    var new_width = base_image_width + scale_move*pixel_scale_rate;
    var new_margin_left = (bodW-new_width)/2 + horizontal_move*pixel_turn_rate;

    horizontal_px_move = base_margin+horizontal_move*pixel_turn_rate;
    scale_px_move = base_image_width+scale_move*pixel_scale_rate;
    margin_left = (bodW-scale_px_move)/2+scale_move*pixel_scale_rate;
    document.getElementById("stream").style.width = `${new_width}px`;
    document.getElementById("stream").style.marginLeft = `${new_margin_left}px`;
}, update_interval);

function set_base_margin(){
    var myImage = new Image();
    var img = document.getElementById("stream");
    myImage.src = img.src;
    var imgW = myImage.width;
    bodW = document.body.clientWidth;
    base_margin = (bodW-imgW)/2;
    document.getElementById("stream").style.marginLeft = `${base_margin}px`;
    document.getElementById("overlay").style.left = `${base_margin}px`;
}