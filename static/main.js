$(function(){
  $('#raise').click(function(){
    $.ajax({
      url: '/',
      data: {'type': '+'},
      type: 'POST',
      success : function(response){
        var temp_should = document.querySelector("#should");
        var resp = JSON.parse(response)
        temp_should.innerHTML = resp.temp_should
      }
    });
  });
});

$(function(){
  $('#lower').click(function(){
    $.ajax({
      url: '/',
      data: {'type': '-'},
      type: 'POST',
      success : function(response){
        var temp_should = document.querySelector("#should");
        var resp = JSON.parse(response)
        temp_should.innerHTML = resp.temp_should
      }
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
    url: '/temp_is',
    type: 'GET',
    dataType: 'json',
    contentType: "application/json",
    success : function(data){
      var temp_is = document.querySelector("#is");
      temp_is.innerHTML = data.value;
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

