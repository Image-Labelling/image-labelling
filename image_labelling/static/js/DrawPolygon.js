const canvas = document.getElementById("displayCanvas");
let ctx;
let vertices = [];

function reset_all() {
    ctx = undefined;
    draw_polygon();
}

function update_vertices(_vtx) {
    resize(vertices, _vtx.length);
    vertices.splice(0, vertices.length, ..._vtx)
}

function draw(_segmentation_id) {
    soft_draw_polygon();
    fetch_polygon(_segmentation_id);

    ctx.lineWidth = 1;
    ctx.strokeStyle = "rgba(255,0,0,0.5)";
    ctx.lineCap = "square";
    ctx.beginPath();

    for (let i = 0; i < vertices.length; i++) {
        if (i === 0) {
            ctx.moveTo(vertices[0]['x'], vertices[0]['y']);
        } else {
            ctx.lineTo(vertices[i]['x'], vertices[i]['y']);
        }
    }

    ctx.lineTo(vertices[0]['x'], vertices[0]['y']);
    add_point(vertices[0]['x'], vertices[0]['y']);
    ctx.closePath();

    ctx.fillStyle = 'rgba(255,0,0,0.5)';

    ctx.fill();
    ctx.stroke();

}

function draw_polygon() {
    let img = new Image();
    img.src = canvas.getAttribute('data-imgsrc');
    img.onload = function () {
        ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
    }
}

function soft_draw_polygon() {
    let img = new Image();
    img.src = canvas.getAttribute('data-imgsrc');

    ctx = canvas.getContext('2d');
    canvas.width = img.width;
    canvas.height = img.height;
    ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
}

function add_point(x, y) {
    ctx.strokeStyle = "rgba(255,0,0,0.5)";
    ctx.fillStyle = "rgba(255,0,0,0.5)";
    ctx.fillRect(x - 2, y - 2, 4, 4);
    ctx.moveTo(x, y);
}

function resize(arr, size) {
    let delta = arr.length - size;

    if (delta > 0) {
        arr.length = size;
    } else {
        while (delta++ < 0) {
            defval = {};
            arr.push(defval);
        }
    }
}

function fetch_polygon(_segmentation_id) {
    let _vertices = [];
    let url = "https://localhost:5000/segmentation?segmentation_id=" + _segmentation_id;
    let request = new XMLHttpRequest();
    request.open('GET', url, true);
    request.responseType = "json";

    request.send();
    let payload;

    request.onreadystatechange = function () {
        if (request.readyState === XMLHttpRequest.DONE && request.status === 200) {
            payload = request.response;

            resize(_vertices, payload.data.length, {x: 0, y: 0})

            for (let i = 0; i < payload.data.length; i++) {
                _vertices[payload.data[i].order]['x'] = payload.data[i].x;
                _vertices[payload.data[i].order]['y'] = payload.data[i].y;
            }

            update_vertices(_vertices);
        }
    }
}
