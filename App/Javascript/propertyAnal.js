"strict";

//Need to write a function that retrieves the data to display on the chart.
//Also need a function that accepts the returned value of the function above and makes a Chart Data object out of it. Then pass it to render chart

//For now, we will have mock data
const deviationChartData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [
    {
      label: "Deviation from Appraisal Value",
      data: [20, 15, -5, 10, -8, 5],
      borderWidth: 1,
      borderColor: "rgba(255, 99, 132, 1)",
    },
  ],
};

// Mock data for age chart
const ageChartData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [
    {
      label: "Influence of Age on Market Value",
      data: [12, 19, 3, 5, 2, 3],
      borderWidth: 1,
      borderColor: "rgba(54, 162, 235, 1)",
    },
  ],
};

// Mock data for land size chart
const landSizeChartData = {
  labels: ["Jan", "Feb", "Mar", "Apr", "May", "Jun"],
  datasets: [
    {
      label: "Sales for Properties of Various Land Sizes",
      data: [120, 90, 110, 100, 80, 120],
      borderWidth: 1,
      borderColor: "rgba(75, 192, 192, 1)",
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

// Render deviation chart
const deviationChart = renderChart("deviation-chart", deviationChartData);

// Render age chart
const ageChart = renderChart("age-chart", ageChartData);

// Render land size chart
const landSizeChart = renderChart("land-size-chart", landSizeChartData);

