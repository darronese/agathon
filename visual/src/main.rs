use anyhow::Result;
use coordinate_altitude::Coord;

mod conversions;
mod elevations;

fn main() -> Result<()> {
    let centre = Coord::new(45.19085, -119.25392);

    let elevations = elevations::get_elevations(centre, 10, 10, 1000.0);

    println!(
        "{:#?}",
        elevations
            .iter()
            .map(|xs| xs
                .iter()
                .map(|x| conversions::metres_to_feet(*x))
                .collect::<Vec<f64>>())
            .collect::<Vec<Vec<f64>>>()
    );

    Ok(())
}
