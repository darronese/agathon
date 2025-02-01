use nannou::prelude::*;

use crate::model::Model;

pub fn view(app: &App, model: &Model, frame: Frame) {
    let draw = app.draw();
    draw.background().color(BLACK);

    for triangle in model.triangles.triangles.chunks(3) {
        let p1 = model.vertices[triangle[0]];
        let p2 = model.vertices[triangle[1]];
        let p3 = model.vertices[triangle[2]];

        draw.line()
            .start(pt3(p1.x, p1.y, p1.z))
            .end(pt3(p2.x, p2.y, p2.z))
            .color(BLACK);
        draw.line()
            .start(pt3(p2.x, p2.y, p2.z))
            .end(pt3(p3.x, p3.y, p3.z))
            .color(BLACK);
        draw.line()
            .start(pt3(p3.x, p3.y, p3.z))
            .end(pt3(p1.x, p1.y, p1.z))
            .color(BLACK);
    }

    draw.to_frame(app, &frame).unwrap();
}
