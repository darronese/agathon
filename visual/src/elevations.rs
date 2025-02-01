use coordinate_altitude::Coord;

use crate::conversions;

pub fn get_elevations(centre: Coord, rows: usize, cols: usize, step: f64) -> Vec<Vec<f64>> {
    let mut coords = (0..rows)
        .map(|i| {
            (0..cols)
                .map(move |j| {
                    Coord::new(
                        centre.latitude
                            + (j as f64 - (cols as f64) / 2.0)
                                * conversions::metres_to_latitude(step),
                        centre.longitude
                            + (i as f64 - (rows as f64) / 2.0)
                                * conversions::metres_to_longitude(step),
                    )
                })
                .collect::<Vec<Coord>>()
        })
        .collect::<Vec<Vec<Coord>>>();

    coords
        .iter_mut()
        .for_each(|row| coordinate_altitude::add_altitude(row).unwrap());

    coords
        .iter()
        .map(|row| row.iter().map(|coord| coord.altitude).collect::<Vec<f64>>())
        .collect()
}
