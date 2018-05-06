var up = 38;
var down = 40;
var right = 39;
var left = 37;
var key_status = {up: 0, down: 0, right: 0, left:0};
var base_margin = 300;
var pixel_turn_rate = 20;

var horizontal_move = 0;
var vertical_move = 0;
var horizontal_px_move = 0;

var update_interval = 25;
var perceived_delay = 750;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function update_hor_with_delay(amount, delay){
    await sleep(delay);
    horizontal_move += amount;
}

var x = setInterval(function() {
    if (key_status[left]){
        horizontal_move += 1;
        update_hor_with_delay(-1, perceived_delay);
    } else if (key_status[right]){
        horizontal_move -= 1;
        update_hor_with_delay(+1, perceived_delay);
    }
    console.log(horizontal_move);
    horizontal_px_move = base_margin+horizontal_move*pixel_turn_rate;
    document.getElementById("stream").style.marginLeft = `${horizontal_px_move}px`;
}, update_interval);

function set_base_margin(){
    var myImage = new Image();
    var img = document.getElementById("stream");
    myImage.src = img.src;
    var imgW = myImage.width;
    var bodW = document.body.clientWidth;
    base_margin = (bodW-imgW)/2;
}
