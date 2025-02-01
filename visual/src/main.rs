use anyhow::Result;
use coordinate_altitude::Coord;
use delaunator::Point;
use macroquad::prelude::*;

mod conversions;
mod elevations;

struct Triangle {
    a: Vec3,
    b: Vec3,
    c: Vec3,
}

#[macroquad::main("Snowpack Visualiser")]
async fn main() -> Result<()> {
    let centre = Coord::new(45.19085, -119.25392);

    let elevations = elevations::get_elevations(centre, 10, 10, 1000.0);

    let mut points = Vec::new();
    let mut positions = Vec::new();

    for (i, row) in elevations.iter().enumerate() {
        for (j, elevation) in row.iter().enumerate() {
            let x = j as f64 * 100.0;
            let y = i as f64 * 100.0;
            let z = *elevation / 1000.0;
            positions.push(vec3(x as f32, y as f32, z as f32));
            points.push(Point { x, y });
        }
    }

    let triangulation = delaunator::triangulate(&points);
    let mut triangles = Vec::new();

    for chunk in triangulation.triangles.chunks(3) {
        if chunk.len() != 3 {
            continue;
        }

        triangles.push(Triangle {
            a: positions[chunk[0]],
            b: positions[chunk[1]],
            c: positions[chunk[2]],
        });
    }

    loop {
        clear_background(BLACK);

        for triangle in triangles.iter() {
            draw_line_3d(triangle.a, triangle.b, WHITE);
            draw_line_3d(triangle.b, triangle.c, WHITE);
            draw_line_3d(triangle.c, triangle.a, WHITE);
        }

        next_frame().await;
    }
}
