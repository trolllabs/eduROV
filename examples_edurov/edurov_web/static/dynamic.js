var MINIMUM_PANEL_WIDTH = 250;
cinema = false;

function set_cinema(cinema_mode){
    if (!cinema_mode){
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "visible";
        panels[1].style.visibility = "visible";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "relative";
        img.style.width = "100%";
        img.style.marginLeft = "0";
    } else {
        var panels = document.getElementsByClassName("side-panel");
        panels[0].style.visibility = "hidden";
        panels[1].style.visibility = "hidden";
        var img = document.getElementsByClassName("center-panel")[0];
        img.style.position = "absolute";
    }
    cinema = cinema_mode
    set_size();
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
    } else {
        var imgDispW = (bodH - 2*pad)*imgR;
        var imgDispH = imgDispW / imgR;
        var panelW = Math.max(parseInt((bodW-2*pad-imgDispW)/2), MINIMUM_PANEL_WIDTH);
        document.getElementsByClassName("grid-container")[0].setAttribute("style",
        `grid-template-columns: ${panelW}px auto ${panelW}px`);

        var realImgW = bodW - 2*panelW - 2*pad;
        var realImhH = realImgW / imgR;

        document.getElementsByClassName("rollOverlay")[0].setAttribute("style",
        `width: ${(bodW - 2*panelW - 2*pad)}px;
        top: ${realImhH/2}px`);
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
