from PySide6.QtWebEngineWidgets import QWebEngineView

class MapWidget(QWebEngineView):
    def __init__(self):
        super().__init__()
        self._loaded = False
        self.loadFinished.connect(self._on_load_finished)
        self.setHtml(self._html())

    def _on_load_finished(self, ok):
        self._loaded = ok

    def update_position(self, lat, lon):
        if not self._loaded:
            return
        self.page().runJavaScript(f"updateGPS({lat}, {lon});")

    def add_marker(self, lat, lon, label="Point"):
        if not self._loaded:
            return
        self.page().runJavaScript(
            f"addUserMarker({lat}, {lon}, `{label}`);"
        )

    def clear_path(self):
        if not self._loaded:
            return
        self.page().runJavaScript("clearRoute();")

    def _html(self):
        return """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<style>
html, body, #map {
    width:100%;
    height:100%;
    margin:0;
}
</style>

<link rel="stylesheet"
 href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
</head>

<body>
<div id="map"></div>

<script>
var map = L.map('map').setView([0,0], 17);

L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{
    maxZoom: 19
}).addTo(map);

var gpsMarker = L.marker([0,0]).addTo(map);

var routeLine = L.polyline([], {
    color: '#00aaff',
    weight: 4
}).addTo(map);

var lastPoint = null;

var redIcon = L.icon({
    iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png',
    shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
    shadowSize: [41, 41]
});

function updateGPS(lat, lon){
    var point = [lat, lon];
    gpsMarker.setLatLng(point);
    map.setView(point, map.getZoom());
    if (!lastPoint || lastPoint[0] !== lat || lastPoint[1] !== lon) {
        routeLine.addLatLng(point);
        lastPoint = point;
    }
}

function addUserMarker(lat, lon, label){
    L.marker([lat, lon], {icon: redIcon})
        .addTo(map)
        .bindPopup(label);
}

function clearRoute(){
    routeLine.setLatLngs([]);
    lastPoint = null;
}
</script>
</body>
</html>
"""
