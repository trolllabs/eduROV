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