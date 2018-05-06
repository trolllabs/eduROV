var up = 38;
var down = 40;
var right = 39;
var left = 37;
var key_status = {up: 0, down: 0, right: 0, left:0}

var horizontal_move = 0;
var vertical_move = 0;

var update_interval = 50;
var perceived_delay = 800;

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

async function update_hor_with_delay(amount, delay){
    console.log("Before delay");
    await sleep(delay);
    horizontal_move += amount;
    console.log("after delay");
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
}, update_interval);

