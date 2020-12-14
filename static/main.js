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
      type: 'POST',
    });
  });
});
