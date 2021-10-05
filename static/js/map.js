
function setForm(name){
  // console.log(document.forms[name].name);
  document.getElementById("current-form").value = name;
  // console.log(document.forms[name].name);
  document.getElementById("current-form").dispatchEvent(new Event("change"))
}
function setPoint(lat,lng){


  // console.log(lat)
  // console.log(lng)
  var form = document.forms[document.getElementById("current-form").value]
  form.elements.lat.value = lat;
  form.elements.long.value = lng;
}



function initAutocomplete() {
  let name =  document.forms[document.getElementById("current-form").value].elements.nombre.value;
  let lat = document.forms[document.getElementById("current-form").value].elements.lat;
  let lng = document.forms[document.getElementById("current-form").value].elements.long;
  if (isNaN(lat.value)){
    lat.value = 0;
  }
  if (isNaN(lng.value)){
    lng.value = 0;
  }
  
  

  let position = { lat: parseFloat(lat.value), lng: parseFloat(lng.value)};

  // console.log(position);
  let map = new google.maps.Map(document.getElementById("map"), {
    center: position,
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

  let center_marker = new google.maps.Marker({
    position: position,
    label: name,
    map: map,
  });
  const contentString =
    '<div id="content">' +
    '<div id="siteNotice">' +
    "</div>" +
    '<h4 id="firstHeading" class="firstHeading">' + name + '</h4>' +
    '<div id="bodyContent">' +
    "<button class='btn btn-small waves-effect waves-light green lighten-1' onclick='setPoint(" + center_marker.getPosition().toJSON().lat + "," + center_marker.getPosition().toJSON().lng + ")'>Guardar esta ubicacion</button>" +
    "</div>" +
  "</div>";
  let infoWindow = new google.maps.InfoWindow({
    content: contentString,
  });
  center_marker.addListener("click", () => {
    infoWindow.open({
      anchor: center_marker,
      map,
      shouldFocus: false,
    });
  });
  // Listen for the event fired when the user selects a prediction and retrieve
  // more details for that place.
  document.getElementById("current-form").addEventListener("change",() => {
    name =  document.forms[document.getElementById("current-form").value].elements.nombre.value;
    lat = document.forms[document.getElementById("current-form").value].elements.lat;
    lng = document.forms[document.getElementById("current-form").value].elements.long;
    changePoint(center_marker,new google.maps.LatLng(lat.value,lng.value),name,infoWindow,map);
  });
  searchBox.addListener("places_changed", () => {
    const places = searchBox.getPlaces();
    if (places.length == 0) {
      return;
    }
    places.forEach((place) => {
      if (!place.geometry || !place.geometry.location) {
        // console.log("Returned place contains no geometry");
        return;
      }
      changePoint(center_marker,place.geometry.location,place.name,infoWindow,map);
    });
  });
  google.maps.event.addListener(map, "click", (event) => {
    changePoint(center_marker,event.latLng,name,infoWindow,map);
  });
  let button = document.getElementById("ok")
  button.addEventListener("click", function() {
      center_marker.getPosition().toJSON()
      lat.value = center_marker.getPosition().toJSON().lat;
      lng.value = center_marker.getPosition().toJSON().lng;
  });

}
function changePoint(marker,location,name,infoWindow,map){
  const bounds = new google.maps.LatLngBounds();

  marker.setPosition(location);
  const contentString =
    '<div id="content">' +
    '<div id="siteNotice">' +
    "</div>" +
    '<h4 id="firstHeading" class="firstHeading">' + name + '</h4>' +
    '<div id="bodyContent">' +
    "<button class='btn btn-small waves-effect waves-light green lighten-1' onclick='setPoint(" + marker.getPosition().toJSON().lat + "," + marker.getPosition().toJSON().lng + ")'>Guardar esta ubicacion</button>" +
    "</div>" +
  "</div>";
  infoWindow.setContent(contentString);

  marker.setLabel(name);


  bounds.extend(location);
  map.fitBounds(bounds);
  map.setZoom(15);
}