const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

//var
let slider_forward;
let slider_hover;
let batteryHtml;

const init = function () {
    slider_forward = document.getElementById("slider_forward");
    slider_hover = document.getElementById("slider_hover");
    batteryHtml = document.getElementById('battery');
    socket.emit('F2B_give_battery');
    listenToElements();
    listenToSocket();
    vraagSettingsOp();
};

const battery_interval = setInterval(function() {
    socket.emit('F2B_give_battery');
}, 5000);

const vraagSettingsOp = function(){
    socket.emit('F2B_settings');
}

const elements = function(){
    slider_forward = document.getElementById("slider_forward");
    slider_hover = document.getElementById("slider_hover");
};

const listenToElements = function(){
    slider_forward.oninput = function() {
        socket.emit('F2B_slider_forward', this.value);
    }
    slider_hover.oninput = function() {
        socket.emit('F2B_slider_hover', this.value);
    }
};

const objectAvoidanceSystems = function() {
    let checkBox = document.getElementById("objectAvoidanceSystems");
    if (checkBox.checked == true){
      socket.emit('F2B_object_avoidance_systems', 'True');
    }
    else {
        socket.emit('F2B_object_avoidance_systems', 'False');
    }
};

const automaticLeds = function() {
    let checkBox = document.getElementById("automaticLeds");
    if (checkBox.checked == true){
      socket.emit('F2B_automatic_leds', 'True');
    }
    else {
        socket.emit('F2B_automatic_leds', 'False');
    }
};

const manualLeds = function() {
    let checkBox = document.getElementById("manualLeds");
    if (checkBox.checked == true){
      socket.emit('F2B_manual_leds', 'True');
    } 
    else {
        socket.emit('F2B_manual_leds', 'False');
    }
};

const listenToSocket = function () {
    socket.on("connect", function () {                  //connect ontvangt hij standaard bij connectie
        console.log("verbonden met socket webserver");
    });
    socket.on('B2F_settings', function(json){
        console.log(json)
        if (json.object_avoidance == false){
            document.getElementById("objectAvoidanceSystems").checked = false;
        }
        else{
            document.getElementById("objectAvoidanceSystems").checked = true;
        }
        if (json.automatic_spots == false){
            document.getElementById("automaticLeds").checked = false;
        }
        else{
            document.getElementById("automaticLeds").checked = true;
        }
        if (json.led_aan == true){
            document.getElementById("manualLeds").checked = true;
        }
        else{
            document.getElementById("manualLeds").checked = false;
        }
    });
    socket.on("B2F_battery", function (value) {                  
        batteryHtml.innerHTML = `${value}%`;
    });
};

document.addEventListener("DOMContentLoaded", init);