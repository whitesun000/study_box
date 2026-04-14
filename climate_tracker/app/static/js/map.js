(function() {
    // HTMLの要素からデータを取得する
    const mapElement = document.getElementById('map');
    if (!mapElement) return;

    // datasetを使ってHTMLから受け取る (Jinja2の構文をJSファイルに書かないための工夫)
    const lat = Number(mapElement.dataset.lat);
    const lon = Number(mapElement.dataset.lon);

    if (isNaN(lat) || isNaN(lon)) {
        console.error("座標データが正しく読み込みませんでした");
        return;
    }

    const map = L.map('map').setView([lat, lon], 10);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    L.marker([lat, lon]).addTo(map)
        .bindPopup('分析対象地点')
        .openPopup();
})();