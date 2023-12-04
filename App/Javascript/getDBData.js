// Javascript script to connect to the server socket and obtain database data

function getDBData(socketQuery){
  let county;
  let startDate;
  let endDate;
  let landSize;
  let propertyAge;
  let householdSize;

  // Page 1: propertyAnalysis.html
  if (socketQuery == "getDeviation")
  {
    county = document.getElementById("county-deviation").value
    startDate = document.getElementById("start-date-deviation").value
    endDate = document.getElementById("end-date-deviation").value
  }
  else if (socketQuery == "getAgeInfluence")
  {
    county = document.getElementById("county-age").value
    startDate = document.getElementById("start-date-age").value
    endDate = document.getElementById("end-date-age").value
    propertyAge = document.getElementById("property-age").value
  }
  else if (socketQuery == "getSaleLandsize")
  {
    county = document.getElementById("county-land").value
    startDate = document.getElementById("start-date-land").value
    endDate = document.getElementById("end-date-land").value
    landSize = document.getElementById("land-size").value
  }
  // Page 2: Affordability
  else if (socketQuery == "getAffordability")
  {
    county = document.getElementById("county").value
    startDate = document.getElementById("start-date").value
    endDate = document.getElementById("end-date").value
    householdSize = document.getElementById("household-size").value
  }
  // Page 3: Neighborhood
  else if (socketQuery == "getSafety")
  {
    county = document.getElementById("county").value
    startDate = document.getElementById("start-date").value
    endDate = document.getElementById("end-date").value
  }
  if (socketQuery == "getDeviation" && (startDate.length == 0 || endDate.length == 0) && county != "default")
  {
    alert("Please add all input.")
  }
  else if (socketQuery == "getAgeInfluence" && (startDate.length == 0 || endDate.length == 0 || propertyAge.length == 0) && county != "default")
  {
    alert("Please add all input.")
  }
  else if (socketQuery == "getSaleLandsize" && (startDate.length == 0 || endDate.length == 0 || landSize.length == 0) && county != "default")
  {
    alert("Please add all input.")
  }
  else if (socketQuery == "getSafety" && (startDate.length == 0 || endDate.length == 0) && county != "default")
  {
    alert("Please add all input.")
  }
  else if (socketQuery == "getAffordability" && (startDate.length == 0 || endDate.length == 0 || county == "default"))
  {
    alert("Please add all input.")
  }
  else {
    let jsonRequest = {
      "requestType": socketQuery,
      "options": {
        "county": county,
        "startDate": startDate,
        "endDate": endDate,
        "landSize": landSize,
        "propertyAge": propertyAge,
        "householdSize" : householdSize,
      }
    }
      // Connect to the application server
      const socket = new WebSocket("ws://10.228.10.193:1337/");

      // Turn the previous JSON text to a string and send it to the server
      socket.addEventListener("open", (event) => {
          socket.send(JSON.stringify(jsonRequest));
      });

      // Receive data from the server
      socket.addEventListener("message", (event) => {
          console.log(event.data)
          if (socketQuery == "getAllTuples")
          {
              document.getElementById("record-count").textContent = event.data + " records";
          }
          // For all other requests: Receive the server's JSON containing dates and values arrays
          else if (socketQuery == "getDeviation")
          {
              // Destroy the previously created chart to add the new one
              if (Chart.getChart("deviation-chart") != null)
              {
                Chart.getChart("deviation-chart").destroy();
              }
              
              console.log(event.data)
              const json = JSON.parse(event.data);
              const deviationChartData = {
                  labels: json.dates,
                  datasets: [
                    {
                      label: "Deviation from Appraisal Value (%)",
                      data: json.values,
                      borderWidth: 1,
                      borderColor: "rgba(255, 99, 132, 1)",
                    },
                  ],
                };
              const deviationChart = renderChart("deviation-chart", deviationChartData);
          }
          else if (socketQuery == "getAgeInfluence")
          { 
              if (Chart.getChart("age-chart") != null)
              {
                Chart.getChart("age-chart").destroy();
              }

              console.log(event.data)
              const json = JSON.parse(event.data);
              const deviationChartData = {
                  labels: json.dates,
                  datasets: [
                    {
                      label: "Influence of Age on Market Value",
                      data: json.values,
                      borderWidth: 1,
                      borderColor: "rgba(255, 99, 132, 1)",
                    },
                  ],
                };
              const deviationChart = renderChart("age-chart", deviationChartData);
          }
          else if (socketQuery == "getSaleLandsize")
          {
              if (Chart.getChart("land-size-chart") != null)
              {
                Chart.getChart("land-size-chart").destroy();
              }

              console.log(event.data)
              const json = JSON.parse(event.data);
              const deviationChartData = {
                  labels: json.dates,
                  datasets: [
                    {
                      label: "Sales for Properties of Various Land Sizes",
                      data: json.values,
                      borderWidth: 1,
                      borderColor: "rgba(255, 99, 132, 1)",
                    },
                  ],
                };
              const deviationChart = renderChart("land-size-chart", deviationChartData);
          }
          else if (socketQuery == "getSafety")
          {
            if (Chart.getChart("sales-chart") != null)
            {
              Chart.getChart("sales-chart").destroy();
            }
            if (Chart.getChart("crime-degree-chart") != null)
            {
              Chart.getChart("crime-degree-chart").destroy();
            }

            console.log(event.data)
            const json = JSON.parse(event.data);
            const degreeCrimeData = {
              labels: json.datesarrests,
              datasets: [
                {
                  label: "Average Arrests",
                  data: json.valuesarrests,
                  borderWidth: 1,
                  borderColor: "rgba(255, 99, 132, 1)",
                },
              ],
            };

            const salesPriceData = {
              labels: json.datessales,
              datasets: [
                {
                  label: "Housing Expense Increase ($) (Mortgage - AVG. Rent)",
                  data: json.valuessales,
                  borderWidth: 1,
                  borderColor: "rgba(54, 162, 235, 1)",
                },
              ],
            };

            const crimeDegreeChart = renderChart("crime-degree-chart", degreeCrimeData);
            const salesPriceChart = renderChart("sales-chart", salesPriceData);
          }
          else if (socketQuery == "getAffordability")
          {
            if (Chart.getChart("affordability-chart") != null)
            {
              Chart.getChart("affordability-chart").destroy();
            }
            
            console.log(event.data)
            const json = JSON.parse(event.data);

            const affordabilityChartData = {
              labels: json.datesafford,
              datasets: [
                {
                  label: "Rent to Mortgage Increase ($)",
                  data: json.valuesafford,
                  borderWidth: 1,
                  borderColor: "rgba(54, 162, 235, 1)",
                },
              ],
            };

            const affordabilityChart = renderChart("affordability-chart", affordabilityChartData);
          }
      });
  }
}
