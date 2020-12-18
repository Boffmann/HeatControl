$(function(){
  $('#raise').click(function(){
    $.ajax({
      url: '/',
      data: {'type': '+'},
      type: 'POST',
    });
  });
});

$(function(){
  $('#lower').click(function(){
    $.ajax({
      url: '/',
      data: {'type': '-'},
      type: 'POST',
    });
  });
});

$(function(){
  $('#onoff').click(function(){
    $.ajax({
      url: '/',
      data: {'type': 'onoff'},
      type: 'POST'
    });
  });
});


function check_status() {
  $.ajax({
    url: '/get_status',
    type: 'GET',
    dataType: 'json',
    contentType: "application/json",
    success : function(data){
      var temp_should = document.querySelector("#should");
      temp_should.innerHTML = data.temp_should;

      if (data.running) {
        $("body").css({"backgroundColor": "#8ec07c"});
      } else {
        $("body").css({"backgroundColor": "#fb4934"});
      }
    },
    error: function(error) {
      console.log(error)
    },
    complete: function(response, textStatus) {
      setTimeout(check_status, 1000);
    }
  });
}

function check_temp() {
  $.ajax({
    url: '/get_temp',
    type: 'GET',
    dataType: 'json',
    contentType: "application/json",
    success : function(data){
      var temp_is = document.querySelector("#is");
      temp_is.innerHTML = data.temp_is;
    },
    error: function(error) {
      console.log(error)
    },
    complete: function(response, textStatus) {
      setTimeout(check_temp, 30000);
    }
  });
}

setTimeout(check_status, 1000);
setTimeout(check_temp, 1000);

