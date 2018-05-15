function cpuTemp(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.stat == 200) {
            alert('The CPU temperature is '+this.responseText);
    };
    xhttp.open("GET", "cpu_temp", true);
    xhttp.send();
}