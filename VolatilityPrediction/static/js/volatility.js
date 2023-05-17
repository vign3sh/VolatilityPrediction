
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
      }
    };
    
    var lineChart = new Chart(speedCanvas, {
      type: 'line',
      data: monthly_data,
      options: chartOptions
    });
  };
  

  const getChartData = () => {
    //console.log("try fetch");
  
        
        const category_data = prediction;
        const [labels, data] = [
          Object.keys(category_data),
          Object.values(category_data),
        ];
        const days=dates;
        renderChart(data, labels, days, 'linechart','Predicted Volatility(5 days)', 'Volatility', '');
      
  };
  

  
  const getChartData1 = () => {
        
    const category_data = returns;
    const [labels, data] = [
      Object.keys(category_data),
      Object.values(category_data),
    ];
    const dates=dates1;
    renderChart(data, labels, dates, 'linechart1','Returns(50 days)', 'Daily Returns(%)', 'Days');
      
  };

  const setdata = () => {

    most_volatile_index = stocknames[stocknames.length - 1][0];
    least_volatile_index = stocknames[0][0];
    const myDiv = document.getElementById("stock_recommendation");
    //console.log(most_volatile_index);
    myDiv.innerHTML =  least_volatile_index + " is the  least volatile index, is recommended for long term inestments.";

  };

var prediction = JSON.parse(document.getElementById('prediction').textContent);
var dates = JSON.parse(document.getElementById('days').textContent);
var returns = JSON.parse(document.getElementById('returns').textContent);
var dates1 = JSON.parse(document.getElementById('days1').textContent);
var stocknames = JSON.parse(document.getElementById('stocknames').textContent);


document.onload = getChartData();
document.onload = getChartData1();




  

