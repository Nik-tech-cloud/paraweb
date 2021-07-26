// FILL LIST OF MOCK FLIGHT POINTS
var jumpPointsList = null;
var leaflet = window.L;
var onlyOneMatchedBefore = false;
var map = leaflet.map("mapid", { doubleClickZoom: false }).locate({ setView: true, maxZoom: 12 });
leaflet.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);


function fillList() {
  var sitelist = document.getElementById("sitelist");
  Object.keys(jumpPointsList).sort().forEach((name) => {
    var point = document.createElement("div");
    point.className = "jumppoint";
    var iconName = "cloud-off";
    switch (jumpPointsList[name]) {
      case "xd":
        break;
    }
    point.innerHTML = `${name} <div data-feather="${iconName}" class="weathericon"></div>`;
    point.setAttribute("name", name);
    point.setAttribute("onclick", "zoomOnPoint(this)");
    // TODO: this is only text, make it remotely beautiful
    sitelist.appendChild(point);
  });
}

function zoomOnPoint(toFind) {
  Object.keys(jumpPointsList).forEach((name) => {
    if (toFind.getAttribute("name") == name) {
      var point = jumpPointsList[name];
      map.flyTo([point.lon, point.lat], 14);
    }
  });
}

function addPoints() {
  Object.keys(jumpPointsList).sort().forEach((name) => {
    var singlepoint = jumpPointsList[name];
    var text = `<div class="popupheader">${name}</div>`;
    if (Object.keys(singlepoint).length > 2) {
      // if we have more than 2 datapoints, get was successful
      if (singlepoint["isWindGood"]) {
        text += "Veter je ugoden";
      } else {
        text += "Veter ni ugoden";
      }
      // add other info
      var slovenianWindDir = singlepoint["windDirection"].replace("S", "J").replace("E", "V").replace("W", "Z").replace("N", "S");
      text += `<br/>Veter piha v smeri ${slovenianWindDir} s hitrostjo ${singlepoint["windSpeed"]} m/s, ter sunki do ${singlepoint["windGust"]} m/s`;
      text += `<br/>Temperatura na vzletišču: ${singlepoint["temperature"]}°C`;

    } else {
      // if data fails to load, display error message
      text += "<br/>Podatkov ni bilo mogoče pridobiti."
    }

    var x = jumpPointsList[name].lon;
    var y = jumpPointsList[name].lat;

    // create weather info popup
    // TODO: make it pretty
    leaflet.marker([x, y]).addTo(map).bindPopup(`${text}`);
  });
}

function setMapToUserLocation(e) {
  var radius = e.accuracy;
  if (radius > 2000) {
    // filter for inaccurate location search
    defaultMapDisplay();
    return;
  }
  leaflet
    .marker(e.latlng)
    .addTo(map)
    .bindPopup(`Vaša lokacija z natančnostjo na ${radius.toFixed(2)}m`);

  leaflet
    .circle(e.latlng, radius, { color: "#ff2919", opacity: "0.4" })
    .addTo(map);
}

function defaultMapDisplay() {
  //default to geographical center of Slovenia, zoom to fit whole country
  map.setView([46.119944, 14.815333], 9);
}

function getPoints() {
  var jumpPointsFromAPI = {}
  try {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open("GET", "http://wecraft75.ddns.net:5000/list", false);
    xmlHttp.send(null);
    jumpPointsFromAPI = JSON.parse(xmlHttp.responseText);
  } catch (e) {
    console.error(e)
  }
  if (jumpPointsFromAPI != {}) {
    jumpPointsList = jumpPointsFromAPI;
  }
  else {
    alert("There was an error loading the list of jump points.");
  }
}

async function getWeatherForPoint(jumpPointName) {
  return new Promise(resolve => {
    var response = {};
    try {
      var xmlHttp = new XMLHttpRequest();
      xmlHttp.open("GET", `http://wecraft75.ddns.net:5000/data?jumpPoint=${jumpPointName}`, false);
      xmlHttp.send(null);
      response = xmlHttp;
    } catch (e) {
      console.error(e)
    }
    if (response.status == 200) {
      response = JSON.parse(xmlHttp.responseText);
    } else {
      response = {};
    }
    resolve(response)
  });
}

async function getWeather(callback) {
  var pointlist = Object.keys(jumpPointsList);
  for (let i = 0; i < pointlist.length; i++) {
    let dataForPoint = await getWeatherForPoint(pointlist[i]);
    Object.keys(dataForPoint).forEach((key) => {
      jumpPointsList[pointlist[i]][key] = dataForPoint[key];
      jumpPointsList[pointlist[i]]["timeAndDate"] = Date.parse(pointlist[i]["timeAndDate"]);
    });
  }
  callback();
}

var afterWeather = () => {
  fillList();
  addPoints();
  // feather icon integration
  feather.replace();
}

// Load app info
getPoints();
getWeather(afterWeather);

// Set event listeners
map.on("locationfound", setMapToUserLocation);
map.on("locationerror", defaultMapDisplay);

// Searchbar filter for sites
function searchElements(inputElement) {
  var toFind = inputElement.value;
  var jumpPoints = document.getElementsByClassName("jumppoint");
  var matching = [];
  // if we find a matching part (of the word), display="", else display="none"
  for (let i = 0; i < jumpPoints.length; i++) {
    var current = jumpPoints[i].getAttribute("name");
    if (current.toLowerCase().indexOf(toFind) > -1) {
      jumpPoints[i].setAttribute("style", "");
      matching.push(jumpPoints[i]);
    }
    else {
      jumpPoints[i].setAttribute("style", "display:none");
    }
  }
  // if we matched exactly one and we didnt before, zoom on that point
  if (matching.length == 1 && !onlyOneMatchedBefore) {
    onlyOneMatchedBefore = true;
    zoomOnPoint(matching[0]);
  }
  // else if we matched more than one, reset matchingBefore
  // do not reset if none matching, or if previously matched 0,
  // this will zoom on point for each letter (zoom only once/dont if we already matched)
  else if (matching.length > 1) {
    onlyOneMatchedBefore = false;
  }
  // if we matched exactly one and we didnt before, zoom on that point
  if (matching.length == 1 && !onlyOneMatchedBefore) {
    onlyOneMatchedBefore = true;
    zoomOnPoint(matching[0]);
  }
  // else if we matched more than one, reset matchingBefore
  // do not reset if none matching, or if previously matched 0,
  // this will zoom on point for each letter (zoom only once/dont if we already matched)
  else if (matching.length > 1) {
    onlyOneMatchedBefore = false;
  }
}
