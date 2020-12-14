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
      type: 'POST',
    });
  });
});
