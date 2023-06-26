// Connect to websocket
console.log("Connecting to http://" + document.domain + ":" + location.port)
var socket = io.connect("http://" + document.domain + ":" + location.port);
console.log("Connected")

//receive details from server
socket.on("live_data", function (msg) {

    // console.log(msg.uptime);
    document.getElementById("uptime").innerHTML = msg.uptime + " hrs";
    // console.log(msg.cpu_usage);
    document.getElementById("cpu_usage").innerHTML = msg.cpu_usage + "%";
    // console.log(msg.cpu_freq);
    document.getElementById("cpu_freq").innerHTML = msg.cpu_freq/1000 + " GHz";
    // console.log(msg.mem_usage);
    document.getElementById("mem_usage").innerHTML = msg.mem_usage + "%";
    // console.log(msg.total_mem);
    document.getElementById("total_mem").innerHTML = "out of " + msg.total_mem + "GB";
});

//receive details from server
socket.on("xmrig_output", function (msg) {

    console.log(msg.xmrig_output);

    // Create new element in id #terminal
    let new_element = document.createElement("p");
    new_element.innerHTML = msg.xmrig_output;
    document.getElementById("terminal").appendChild(new_element);

});