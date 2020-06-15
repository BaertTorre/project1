const lanIP = `${window.location.hostname}:5000`;
const socket = io(`http://${lanIP}`);

let screenHeight

const init = function () {
    screenHeight = screen.availHeight;
    listenToSocket();
};

const listenToSocket = function () {
    socket.on("connect", function () {                  //connect ontvangt hij standaard bij connectie
        console.log("verbonden met socket webserver");
        socket.emit('F2B_give_history_list')
    });

    socket.on("B2F_history_list", function (data) {
        console.log(data)
    });
};

document.addEventListener("DOMContentLoaded", init);