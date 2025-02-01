use coordinate_altitude::Coord;
use delaunator::{Point, Triangulation};
use nannou::prelude::*;

use crate::{elevations, settings, view};

pub struct Model {
    pub vertices: Vec<Vec3>,
    pub triangles: Triangulation,
}

pub fn model(app: &App) -> Model {
    let window_id = app
        .new_window()
        .resizable(false)
        .size(settings::WINDOW_WIDTH, settings::WINDOW_HEIGHT)
        .title(" Visualization")
        .view(view::view)
        // .raw_event(event::raw_window_event)
        .build()
        .unwrap();

    let window = app.window(window_id).unwrap();

    // let egui = Egui::from_window(&window);

    let rows = 10;
    let cols = 10;

    let elevations =
        elevations::get_elevations(Coord::new(45.19085, -119.25392), rows, cols, 1000.0);

    let mut vertices = vec![];
    let mut points = vec![];

    for (i, row) in elevations.iter().enumerate() {
        for (j, elevation) in row.iter().enumerate() {
            let z = *elevation as f32 / 5000.0;

            vertices.push(Vec3::new(i as f32, j as f32, z));
            points.push(Point {
                x: i as f64,
                y: j as f64,
            });
        }
    }

    let triangles = delaunator::triangulate(&points);

    Model {
        vertices,
        triangles,
    }
}
