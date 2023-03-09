function ajaxGetRequest(path, callback){
  let request = new XMLHttpRequest();
  request.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200){
        callback(this.response);
    }
  };
  request.open("GET", path);
  request.send();
}

function ajaxPostRequest(path, data, callback){
  let request = new XMLHttpRequest();
  request.onreadystatechange = function(){
    if (this.readyState === 4 && this.status === 200){
      callback(this.response);
    }
  };
  request.open("POST", path);
  request.send(data);
}

function getData() {
  ajaxGetRequest("/bar", displayBars);
}

function displayBars(response){
  let dict = JSON.parse(response)
  let states = [];
  let percents = [];
  for(let keys of Object.keys(dict)) {
    states.push(keys)
    percents.push(Number(dict[keys]))
    let data =[{
      "x": states,
      "y": percents,
     "type": 'bar'
    }];
    let layout = {
      title: 'Fully Vaccinated By Location',
      xaxis: {title: "Location"},
      yaxis: {title: "% Fully Vaccinated"}
    }
    Plotly.newPlot('bar', data, layout)
  }
}

function getData() {
  ajaxGetRequest("/bar", displayBars);
  ajaxGetRequest("/pie", displayPie)
}

function displayPie(response) {
  let dict = JSON.parse(response)
  let totals = [];
  let names = [];
  for(let keys of Object.keys(dict)) {
    totals.push(Number(keys))
    names.push(dict[keys])
  let data = [{
    "values": totals,
    "labels": names,
    "type": 'pie',
    "name": 'Vaccine Manufacturer Market Share'
  }];
  let layout = {
    title: 'Vaccine Manufacturer Market Share',
    height: 400,
    width: 500
  };
  Plotly.newPlot('pie', data, layout);
}
}

function getLocData(){
  let div_ele = document.getElementById('locText')
  let lo = div_ele["value"]
  let loc = JSON.stringify(lo)
  ajaxPostRequest("/line", loc, displayLine)
}

function displayLine(response) {
  let dict = JSON.parse(response)
  let dates = [];
  let percents = [];
  for(let keys of Object.keys(dict)) {
    dates.push(keys)
    percents.push(Number(dict[keys]))
    let data = [{
      "x": dates,
      "y": percents
    }];
    let layout = {
    title: '% of Location Fully Vaccinated By Date',
    xaxis: {
      title: 'Date',
    },
    yaxis: {
      title: '% Fully Vaccinated',
    }
    };
    Plotly.newPlot('line', data, layout)
}
}
