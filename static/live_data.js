// Connect to websocket
console.log("Connecting to http://" + document.domain + ":" + location.port)
var socket = io.connect("http://" + document.domain + ":" + location.port);
console.log("Connected")

//receive details from server
socket.on("live_data", function (msg) {
    // Get element with id: moisture_level, and set its innerHTML to msg.data

    console.log(msg.uptime);
    document.getElementById("uptime").innerHTML = msg.uptime;
    console.log(msg.cpu_usage)
    document.getElementById("cpu_usage").innerHTML = msg.cpu_usage;
});