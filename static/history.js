var chart_config = {
  type: 'line',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    responsive: true,
    legend: {
      display: false
    },
    plugins: {
      title: {
        display: true,
        text: 'Zeitlicher Temperaturverlauf'
      },
      tooltip: {
        mode: 'index',
        intersect: false
      }
    },
    hover: {
      mode: 'nearest',
      intersect: false
    },
    scales: {
      xAxes: [{
        ticks: {
          maxTicksLimit: 30
        }
      }],
      x: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Zeit'
        }
      },
      y: {
        display: true,
        scaleLabel: {
          display: true,
          labelString: 'Temperatur'
        }
      }
    }
  }
};

to_date_string = function(timestamp) {
  var date = new Date(timestamp * 1000);
  var hours = "0" + date.getHours();
  var minutes = "0" + date.getMinutes();
  var seconds = "0" + date.getSeconds();
  var day = "0" + date.getDate();
  var month = "0" + date.getMonth() + 1;

  return day.substr(-2) + "." + month.substr(-2) + ". " + hours.substr(-2) + ":" + minutes.substr(-2) + ":" + seconds.substr(-2);
}

var socket = io('/state')
socket.on('connect', function() {
  socket.emit('get_since_start')
});

socket.on('since_start', function(data) {
  var ctx = document.getElementById('canvas').getContext('2d');
  window.myLine = new Chart(ctx, chart_config);
  console.log("Since Start");

  values = data['values'];

  // Add new dataset
  var newDataset = {
    label: 'Temps',
    backgroundColor: '#FB4934',
    borderColor: '#FB4934',
    data: [],
    fill: false
  };

  values.forEach(function(item, index) {
    chart_config.data.labels.push(to_date_string(item[0]));
    newDataset.data.push(item[1]);
  });

  chart_config.data.datasets.push(newDataset);
  window.myLine.update();
});

socket.on('temp_is', function(json) {
  chart_config.data.labels.push(to_date_string(json['timestamp']));
  chart_config.data.datasets[0].data.push(json['temp_is']);
  window.myLine.update();
});


