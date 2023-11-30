// Javascript script to connect to the server socket and obtain database data

function getDBData(socketQuery){
  let county;
  let startDate;
  let endDate;

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
  }
  else if (socketQuery == "getSaleLandsize")
  {
    county = document.getElementById("county-land").value
    startDate = document.getElementById("start-date-land").value
    endDate = document.getElementById("end-date-land").value
  }

  let jsonRequest = {
    "requestType": socketQuery,
    "options": {
      "county": county,
      "startDate": startDate,
      "endDate": endDate
    }
  }
  
    const socket = new WebSocket("ws://10.228.10.193:1337/");

    socket.addEventListener("open", (event) => {
        socket.send(JSON.stringify(jsonRequest));
    });

    socket.addEventListener("message", (event) => {
        console.log(event.data)
        if (socketQuery == "getAllTuples")
        {
            document.getElementById("record-count").textContent = event.data + " records";
        }
        else if (socketQuery == "getDeviation")
        {
            console.log(event.data)
            const json = JSON.parse(event.data);
            const deviationChartData = {
                labels: json.date,
                datasets: [
                  {
                    label: "Deviation from Appraisal Value",
                    data: json.counts,
                    borderWidth: 1,
                    borderColor: "rgba(255, 99, 132, 1)",
                  },
                ],
              };
            const deviationChart = renderChart("deviation-chart", deviationChartData);
        }
    });
}
