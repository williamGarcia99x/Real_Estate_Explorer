"strict";

//Need to write a function that retrieves the data to display on the chart.
//Also need a function that accepts the returned value of the function above and makes a Chart Data object out of it. Then pass it to render chart

//For now, we will have mock data
const affordabilityChartData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [
    {
      label: "Average Housing Expenses",
      data: [20, 15, -5, 10, -8, 5],
      borderWidth: 1,
      borderColor: "rgba(255, 99, 132, 1)",
    },
    {
        label: "Predicted Monthly Housing Cost",
        data: [12, 19, 3, 5, 2, 3],
        borderWidth: 1,
        borderColor: "rgba(54, 162, 235, 1)",
      },
  ],
};


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

// Render affordability chart
const affordabilityChart = renderChart("affordability-chart", affordabilityChartData);


