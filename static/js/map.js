
function setForm(name){
  document.getElementById("current-form").innerHTML = document.forms[name].name;

  console.log(document.forms[name].name);
}
function setPoint(lat,lng){
  

  console.log(lat)
  console.log(lng)
  var form = document.forms[document.getElementById("current-form").innerHTML]
  form.elements.latittude.value = lat;
  form.elements.longittude.value = lng;
}

let map;

function initMap() {
  map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -34.397, lng: 150.644 },
    zoom: 8,
  });
}

function initAutocomplete() {
  let map = new google.maps.Map(document.getElementById("map"), {
    center: { lat: -33.8688, lng: 151.2195 },
    zoom: 13,
    mapTypeId: "roadmap",
  });
  // Create the search box and link it to the UI element.
  const input = document.getElementById("pac-input");
  const searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);
  // Bias the SearchBox results towards current map's viewport.
  map.addListener("bounds_changed", () => {
    searchBox.setBounds(map.getBounds());
  });
  let markers = [];
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();

    if (places.length == 0) {
      return;
    }
    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];
    // For each place, get the icon, name and location.
    const bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        console.log("Returned place contains no geometry");
        return;
      }
      
      const contentString =
        '<div id="content">' +
        '<div id="siteNotice">' +
        "</div>" +
        '<h1 id="firstHeading" class="firstHeading">' + place.name + '</h1>' +
        '<div id="bodyContent">' +
        "<button class='btn btn-small waves-effect waves-light green lighten-1' onclick='setPoint(" + place.geometry.location.lat() + "," +  place.geometry.location.lng() + ")'>Guardar esta ubicacion</button>" +
        "</div>" +
      "</div>";
      const infowindow = new google.maps.InfoWindow({
        content: contentString,
      });

      // Create a marker for each place.
      let marker = new google.maps.Marker({
        map,
        title: place.name,
        position: place.geometry.location,
      })

      marker.addListener("click", () => {
        infowindow.open({
          anchor: marker,
          map,
          shouldFocus: false,
        });
      })
      // Create a marker for each place.
      

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });
}



var polygonArray = [];
function editMap() {
  const map = new google.maps.Map(document.getElementById("map"), {
          
      zoom: 11.75,
      center: { lat: -31.4067538, lng:-64.2041696},
      mapTypeId: "terrain",
  });
  var polygonArray = [];
  const drawingManager = new google.maps.drawing.DrawingManager({
      drawingMode: google.maps.drawing.OverlayType.MARKER,
      drawingControl: true,
      drawingControlOptions: {
      position: google.maps.ControlPosition.TOP_CENTER,
      drawingModes: [
          google.maps.drawing.OverlayType.MARKER,
          google.maps.drawing.OverlayType.CIRCLE,
          google.maps.drawing.OverlayType.POLYGON,
          google.maps.drawing.OverlayType.POLYLINE,
          google.maps.drawing.OverlayType.RECTANGLE,
      ],
      },
      markerOptions: {
      icon: "https://developers.google.com/maps/documentation/javascript/examples/full/images/beachflag.png",
      },
      circleOptions: {
      fillColor: "#ffff00",
      fillOpacity: 1,
      strokeWeight: 5,
      clickable: false,
      editable: true,
      zIndex: 1,
      },
  });

  drawingManager.setMap(map);

  google.maps.event.addListener(drawingManager, 'polygoncomplete', function (polygon) {
      // assuming you want the points in a div with id="info"
      document.getElementById('info').innerHTML += "polygon points:" + "<br>";
      for (var i = 0; i < polygon.getPath().getLength(); i++) {
          document.getElementById('info').innerHTML += polygon.getPath().getAt(i).toUrlValue(6) + "<br>";
      }
      polygonArray.push(polygon);
      console.log(polygon)

  });
}