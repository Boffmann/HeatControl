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


function periodically() {
  $.ajax({
    url: '/get_status',
    type: 'GET',
    dataType: 'json',
    contentType: "application/json",
    success : function(data){
      var temp_is = document.querySelector("#is");
      var temp_should = document.querySelector("#should");
      temp_is.innerHTML = data.temp_is;
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
      setTimeout(periodically, 1000);
    }
  });
}

setTimeout(periodically, 1000);

