
const renderChart = (data, labels, months, indexname, title, ylabel, xlabel) => {
    var speedCanvas = document.getElementById(indexname);
    
  
   var datasets=[];
    const backgroundColor= [
      "rgba(255, 99, 132, 0.2)",
      "rgba(54, 162, 235, 0.2)",
      "rgba(255, 206, 86, 0.2)",
      "rgba(75, 192, 192, 0.2)",
      "rgba(153, 102, 255, 0.2)",
      "rgba(255, 159, 64, 0.2)",
    ];
    const borderColor= [
      "rgba(255, 99, 132, 1)",
      "rgba(54, 162, 235, 1)",
      "rgba(255, 206, 86, 1)",
      "rgba(75, 192, 192, 1)",
      "rgba(153, 102, 255, 1)",
      "rgba(255, 159, 64, 1)",
    ];
  
    data.forEach(myFunction)
  
    function myFunction(item, index, arr) {
      var data_dict={
        'label':labels[index],
        'data':item,
        'backgroundColor':backgroundColor[index],
        'borderColor':borderColor[index]
      };
  
      datasets[index]=data_dict
    }
    
    //console.log("datasets", datasets);
  
  
    var monthly_data = {
      labels: months,
      datasets:datasets
    };
    
    var chartOptions = {
      responsive: true,
      maintainAspectRatio: false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      plugins: {
        title: {
          display: true,
          text: title
        }
      },
      scales: {
        y: {
          title: {
            display: true,
            text: ylabel
          }
        },
        x: {
          title: {
            display: true,
            text: xlabel
          }
        }
      },
      
    };
    
    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: monthly_data,
      options: chartOptions
    });
  };
  

  
  const getChartData = (returns,dates) => {        
    const category_data = returns;
    const [labels, data] = [
      Object.keys(category_data),
      Object.values(category_data),
    ];
  renderChart(data, labels, dates, 'linechart','Returns(250 days)','Daily Returns(%)', 'Days');
  };
  
  const getChartData1 = (returns,dates) => {        
    const category_data = returns;
    const [labels, data] = [
      Object.keys(category_data),
      Object.values(category_data),
    ];
  renderChart(data, labels, dates, 'linechart1','Stock Price(250 days)', 'Daily Stock Price', 'Days');
  };




var returns = JSON.parse(document.getElementById('returns').textContent);
var dates = JSON.parse(document.getElementById('days1').textContent);
var price = JSON.parse(document.getElementById('price').textContent);

document.onload = getChartData(returns,dates);
document.onload = getChartData1(price,dates);


  

