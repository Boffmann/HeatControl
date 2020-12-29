
// var socket = io.connect('http://' + document.domain + ':' + location.port);
var socket = io('/state')
socket.on('connect', function() {
  // Pass
});

socket.on('state', function(data) {
  var temp_should = document.querySelector("#should");
  temp_should.innerHTML = data.temp_should;

  var isHeating = document.querySelector("#isHeating");
  if (data.running) {
    $("body").css({"backgroundColor": "#8ec07c"});
  } else {
    $("body").css({"backgroundColor": "#fb4934"});
  }
  if (data.heating) {
    isHeating.innerHTML = "Heizt...";
  } else {
    isHeating.innerHTML = "";
  }
});

socket.on('temp_is', function(data) {
  var temp_is = document.querySelector("#is");
  temp_is.innerHTML = data.temp_is;
});

$(function(){
  $('#raise').click(function(){
    socket.emit('raise')
  });
});

$(function(){
  $('#lower').click(function(){
    socket.emit('lower')
  });
});

$(function(){
  $('#onoff').click(function(){
    socket.emit('onoff')
  });
});
