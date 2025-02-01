pub fn metres_to_feet(metres: f64) -> f64 {
    metres * 3.28084
}

// NOTE:
// metres = cos(latitude) * 111,000 metres
// metres = longitude * 111,000 metres
pub fn metres_to_longitude(metres: f64) -> f64 {
    metres / 111_000.0
}

pub fn metres_to_latitude(metres: f64) -> f64 {
    (metres / 111_000.0).acos()
}
