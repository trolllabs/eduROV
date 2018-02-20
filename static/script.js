var last_key;
var pressed_keys = {};

document.onkeydown = function(evt) {
    evt = evt || window.event;
    if (evt.keyCode != last_key){
        pressed_keys[evt.keyCode] = 1;
        console.log(pressed_keys)
        lastkey = evt.keyCode;
    }
};

document.onkeyup = function(evt) {
    delete pressed_keys[evt.keyCode];
    console.log(pressed_keys)
    last_key = 0;
};

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