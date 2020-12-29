var socket = io('/history')
socket.on('connect', function() {
  socket.emit('get_since_start')
});

socket.on('temp_is', function(data) {
  var temp_is = document.querySelector("#test");
  temp_is.innerHTML = data.temp_is;
});
