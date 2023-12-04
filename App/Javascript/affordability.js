"strict";

//Need to write a function that retrieves the data to display on the chart.
//Also need a function that accepts the returned value of the function above and makes a Chart Data object out of it. Then pass it to render chart

//For now, we will have mock data

function renderChart(canvasId, chartData) {
  const ctx = document.getElementById(canvasId).getContext("2d");
  return new Chart(ctx, {
    type: "line",
    data: chartData,
    options: {
      scales: {
        y: {
          beginAtZero: true,
        },
      },
    },
  });
}


