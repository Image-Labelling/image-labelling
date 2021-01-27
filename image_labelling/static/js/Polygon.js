let vertices = [];
let ctx; // context
let _closed = false;
const canvas = document.getElementById("labelCanvas");


function reset_all() {
    vertices = [];
    ctx = undefined;
    _closed = false;
    draw_polygon(true);
    if (vertices.length === 0) {
        document.getElementById('coords').value = '';

    } else {
        document.getElementById('coords').value = JSON.stringify(vertices);
    }

}

function undo() {
    ctx = undefined;
    vertices.pop();
    _closed = false;
    draw_polygon(true);
    if (vertices.length === 0) {
        document.getElementById('coords').value = '';

    } else {
        document.getElementById('coords').value = JSON.stringify(vertices);
    }

}


function add_point(x, y) {
    ctx.strokeStyle = "rgba(255,0,0,0.5)";
    ctx.fillStyle = "rgba(255,0,0,0.5)";
    ctx.fillRect(x - 2, y - 2, 4, 4);
    ctx.moveTo(x, y);
}

function _intersects(a, b, c, d) {
    const f = (-(d['x'] - c['x']) * (b['y]'] - a['y']) + (b['x'] - a['x']) * (d['y'] - c['y']));
    const s = (-(b['y]'] - a['y']) * (a['x'] - c['x']) + (b['x'] - a['x']) * (a['y'] - c['y'])) / f;
    const t = (+(d['x'] - c['x']) * (a['y'] - c['y']) - (d['y'] - c['y']) * (a['x'] - c['x'])) / f;
    return (s >= 0 && s <= 1 && t >= 0 && t <= 1);
}

function draw(end) {
    ctx.lineWidth = 1;
    ctx.strokeStyle = "rgba(255,0,0,0.5)";
    ctx.lineCap = "square";
    ctx.beginPath();

    for (let i = 0; i < vertices.length; i++) {
        if (i === 0) {
            ctx.moveTo(vertices[0]['x'], vertices[0]['y']);
            end || add_point(vertices[0]['x'], vertices[0]['y']);
        } else {
            ctx.lineTo(vertices[i]['x'], vertices[i]['y']);
            end || add_point(vertices[i]['x'], vertices[i]['y']);
        }
    }
    if (end) {
        ctx.lineTo(vertices[0]['x'], vertices[0]['y']);
        ctx.closePath();

        ctx.fillStyle = 'rgba(255,0,0,0.5)';

        ctx.fill();
        _closed = true;
    }


    ctx.stroke();

    if (vertices.length === 0) {
        document.getElementById('coords').value = '';

    } else {
        document.getElementById('coords').value = JSON.stringify(vertices);
    }

}

function check_intersecting(x, y) {
    if (vertices.length < 4) {
        return false;
    }

    let a = [];
    let b = [];
    let c = [];
    let d = [];

    c['x'] = vertices[vertices.length - 1]['x'];
    c['y'] = vertices[vertices.length - 1]['y'];
    d['x'] = x;
    d['y'] = y;

    for (let i = 0; i < vertices.length - 1; i++) {
        a['x'] = vertices[i]['x'];
        a['y'] = vertices[i]['y'];
        b['x'] = vertices[i + 1]['x'];
        b['y'] = vertices[i + 1]['y'];
        if (b['x'] === c['x'] && b['y'] === c['y']) {
            continue;
        }
        if (a['x'] === d['x'] && a['y'] === d['y']) {
            continue;
        }
        if (_intersects(a, b, c, d)) {
            return true;
        }

    }
    return false;
}

function new_segment() {
    if (_closed) {
        alert("Can't add vertices to a closed polygon.");
        return false;
    }

    var rect, x, y;

    if (event.ctrlKey || event.button === 2 || event.which === 3) {
        if (vertices.length < 3) {
            alert('A minimum of 3 vertices is needed to make a polygon');
            return false;
        }
        x = vertices[0]['x'];
        y = vertices[0]['y'];
        if (check_intersecting(x, y)) {
            alert("Unable to close polygon, intersecting lines");
            return false;
        }
        draw(true);
        event.preventDefault();
        return false;
    } else {
        rect = canvas.getBoundingClientRect();
        x = event.clientX - rect.left;
        y = event.clientY - rect.top;
        if (vertices.length > 0 && x === vertices[vertices.length - 1]['x'] && y === vertices[vertices.length - 1]['y']) {
            return false;
        }
        if (check_intersecting(x, y)) {
            alert("Unable to add point, intersecting lines");
            return false;
        }

        vertices.push({'x': x, 'y': y});
        draw(false);
        return false;
    }
}

function draw_polygon(_draw) {
    let img = new Image();
    img.src = canvas.getAttribute('data-imgsrc');
    img.onload = function () {
        ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        if (_draw) {
            draw(false);
        }
    }
}

function submit() {
    if (!_closed) {
        alert("Polygon is not completed yet.")
        return false;
    }
    $.ajax({
        type: 'post',
        crossDomain: true,
        contentType: 'application/json',
        data: JSON.stringify(vertices)
    })
    $("#btnSubmit").attr("disabled", true);
}
