const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let speed;
let googleMap;
let batteryHtml;

const init = function () {
    speed = document.getElementById("speed");
    googleMap = document.getElementById("googleMap");
    batteryHtml = document.getElementById('battery');
    listenToSocket();
    console.log('give location');
    socket.emit('F2B_give_location');
    socket.emit('F2B_give_battery');
};

const location_interval = setInterval(function() {
    console.log('give location');
    socket.emit('F2B_give_location');
    socket.emit('F2B_give_battery');
}, 5000);

const listenToSocket = function () {
    socket.on("connect", function () {                  //connect ontvangt hij standaard bij connectie
        console.log("verbonden met socket webserver");
    });

    socket.on("B2F_coordinaten", function (value) {
        console.log(value);
        let screenHeight = $(window).height() - 45;
        googleMap.innerHTML = `<iframe width="100%" height="${screenHeight}" frameborder="0" style="border:0" src="https://www.google.com/maps/embed/v1/place?key=AIzaSyD35aYe371FvGW0oGO82bPGqmWqevesKWY
        &q=${value.coor[0]},${value.coor[1]}&maptype=satellite&zoom=21" allowfullscreen>
            </iframe>`;
        speed.innerHTML = `${value.coor[2]} Km/H`;
    });

    socket.on("B2F_battery", function (value) {                  
        batteryHtml.innerHTML = `${value}%`;
    });
};

document.addEventListener("DOMContentLoaded", init);