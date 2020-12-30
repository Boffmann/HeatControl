var chart_config = {
  type: 'line',
  data: {
    labels: [],
    datasets: []
  },
  options: {
    responsive: true,
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
    chart_config.data.labels.push(item[0]);
    newDataset.data.push(item[1]);
  });

  chart_config.data.datasets.push(newDataset);
  window.myLine.update();
});

socket.on('temp_is', function(json) {
  chart_config.data.labels.push(json['timestamp']);
  chart_config.data.datasets[0].data.push(json['temp_is']);
  window.myLine.update();
});


