function showCurrentTime() {
    var today = new Date();
    var time = "เวลา " + today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds() + " น.";
    document.getElementById('currentTime').innerHTML = time;
}
setInterval(showCurrentTime, 1000);